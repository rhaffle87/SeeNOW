# core/browser_engine.py
import io
import os
import sys
import time
import base64
import logging
import hashlib
import asyncio
import subprocess
from typing import Optional, List, Dict, Any, Tuple, Union
from PIL import Image
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Frame

logger = logging.getLogger("SeeNOW.Browser")

def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_path, relative_path)

class BrowserEngine:
    def __init__(self, config_manager=None):
        self.config = config_manager
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.active_frame: Optional[Union[Page, Frame]] = None
        self.chrome_process: Optional[subprocess.Popen] = None

        self.som_path = resource_path(os.path.join("core", "som_injector.js"))
        if not os.path.isfile(self.som_path):
            alt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core", "som_injector.js")
            if os.path.isfile(alt_path):
                self.som_path = alt_path

        with open(self.som_path, "r", encoding="utf-8") as f:
            self.som_script = f.read()

    @staticmethod
    def find_chrome_executable() -> Optional[str]:
        if sys.platform == "win32":
            paths = [
                os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
                os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
                os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
                os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
                os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
            ]
            for p in paths:
                if os.path.isfile(p):
                    return p
        elif sys.platform == "darwin":
            paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
            ]
            for p in paths:
                if os.path.isfile(p):
                    return p
        else:
            paths = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium"]
            for p in paths:
                if os.path.isfile(p):
                    return p
        return None

    def launch_debug_browser(self, cdp_port: int = 9222) -> bool:
        exe = self.find_chrome_executable()
        if not exe:
            logger.error("Eksekutabel Google Chrome atau Microsoft Edge tidak ditemukan di sistem.")
            return False

        if getattr(sys, "frozen", False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        profile_dir = os.path.join(base_dir, "chrome_profile")
        os.makedirs(profile_dir, exist_ok=True)

        cmd = [
            exe,
            f"--remote-debugging-port={cdp_port}",
            f"--user-data-dir={profile_dir}",
            "--no-first-run",
            "--no-default-browser-check"
        ]

        try:
            self.chrome_process = subprocess.Popen(cmd)
            time.sleep(1.2)
            logger.info(f"Browser berhasil diluncurkan dengan port {cdp_port}")
            return True
        except Exception as e:
            logger.error(f"Gagal meluncurkan browser: {e}")
            return False

    async def connect_cdp(self, cdp_url: str = "http://localhost:9222") -> Page:
        if not self.playwright:
            self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.connect_over_cdp(cdp_url)
        contexts = self.browser.contexts
        if contexts:
            self.context = contexts[0]
        else:
            self.context = await self.browser.new_context()

        pages = self.context.pages
        if pages:
            self.page = pages[0]
        else:
            self.page = await self.context.new_page()

        if self.config and self.config.get("prevent_blur_detection", True):
            await self.apply_anti_blur_stealth(self.page)

        return self.page

    async def is_connection_alive(self) -> bool:
        if not self.browser:
            return False

        if self.context:
            try:
                pages = self.context.pages
                if self.page is None or self.page.is_closed():
                    alive_pages = [p for p in pages if not p.is_closed()]
                    if alive_pages:
                        self.page = alive_pages[-1]
                        self.active_frame = self.page
                        logger.info("Beralih ke tab browser aktif yang masih terbuka.")
                    else:
                        self.page = None
                        self.active_frame = None
                        return False
            except Exception:
                self.page = None
                self.browser = None
                self.active_frame = None
                return False

        if not self.page or self.page.is_closed():
            return False

        try:
            await self.page.evaluate("() => true")
            return True
        except Exception as e:
            logger.warning(f"Koneksi browser/tab terputus: {e}")
            self.page = None
            self.browser = None
            self.active_frame = None
            return False

    async def apply_anti_blur_stealth(self, page: Page):
        stealth_js = """
        (() => {
            try {
                Object.defineProperty(document, 'visibilityState', { get: () => 'visible', configurable: true });
                Object.defineProperty(document, 'hidden', { get: () => false, configurable: true });
                window.addEventListener('blur', (e) => e.stopImmediatePropagation(), true);
                window.addEventListener('visibilitychange', (e) => e.stopImmediatePropagation(), true);
                document.addEventListener('visibilitychange', (e) => e.stopImmediatePropagation(), true);
            } catch(e) {}
        })();
        """
        try:
            await page.add_init_script(stealth_js)
            await page.evaluate(stealth_js)
        except Exception as e:
            logger.warning(f"Gagal menyuntikkan script anti-blur: {e}")

    async def find_best_quiz_frame(self) -> Optional[Union[Page, Frame]]:
        if not self.page:
            return None

        frames = self.page.frames
        if len(frames) == 1:
            self.active_frame = self.page
            return self.page

        best_frame: Union[Page, Frame] = self.page
        max_inputs = -1

        for f in frames:
            try:
                count = await f.evaluate("""
                    () => document.querySelectorAll('input[type="radio"], input[type="checkbox"], [role="radio"], [role="checkbox"], .option').length
                """)
                if count > max_inputs:
                    max_inputs = count
                    best_frame = f
            except Exception:
                continue

        self.active_frame = best_frame
        return best_frame

    async def capture_som_state(self) -> Tuple[str, List[Dict[str, Any]], str]:
        if not self.page:
            raise RuntimeError("Browser belum terhubung.")

        target = await self.find_best_quiz_frame()
        if not target:
            raise RuntimeError("Tidak dapat menemukan frame kuis.")
        await target.evaluate(self.som_script)
        elements = await target.evaluate("window.injectSoM()")

        # Penanganan viewport: auto-scroll jika elemen terlalu sedikit atau tidak ada tombol navigasi
        def has_navigation_candidate(els: List[Dict[str, Any]]) -> bool:
            nav_keywords = ("next", "selanjutnya", "berikut", "lanjut", "submit", "kirim", "jawab", "finish", "selesai")
            for e in els:
                t = (e.get("text") or "").lower()
                role = (e.get("role") or "").lower()
                tag = (e.get("tag") or "").lower()
                if any(kw in t for kw in nav_keywords) or role == "button" or tag == "button":
                    return True
            return False

        if len(elements) < 2 or not has_navigation_candidate(elements):
            try:
                scrolled = await target.evaluate("""
                    () => {
                        if (document.documentElement.scrollHeight > window.innerHeight) {
                            window.scrollBy(0, 350);
                            return true;
                        }
                        return false;
                    }
                """)
                if scrolled:
                    await asyncio.sleep(0.12)
                    await target.evaluate(self.som_script)
                    elements = await target.evaluate("window.injectSoM()")
            except Exception:
                pass

        # Ambil screenshot JPEG 70%
        raw_bytes = await self.page.screenshot(type="jpeg", quality=70, full_page=False)

        # Kompresi bandwidth cerdas: Batasi resolusi maksimal lebar 1280px jika layar ultra-HD
        try:
            with Image.open(io.BytesIO(raw_bytes)) as pil_img:
                w, h = pil_img.size
                if w > 1280:
                    new_w = 1280
                    new_h = int(h * (1280 / w))
                    resized_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    buf = io.BytesIO()
                    resized_img.save(buf, format="JPEG", quality=70, optimize=True)
                    raw_bytes = buf.getvalue()
        except Exception:
            pass

        screenshot_b64 = base64.b64encode(raw_bytes).decode("utf-8")

        # Hapus overlay visual saja, pertahankan data-som-id untuk locator
        await target.evaluate("window.removeSoM(false)")

        summary_lines = []
        for el in elements:
            summary_lines.append(
                f"[{el['id']}] Tag: <{el['tag']}> Type: '{el['type']}' Text: \"{el['text']}\""
            )
        elements_summary = "\n".join(summary_lines)

        return screenshot_b64, elements, elements_summary

    async def preview_som_overlay(self, duration_seconds: float = 3.0):
        if not self.page:
            raise RuntimeError("Browser belum terhubung.")

        target = await self.find_best_quiz_frame()
        if not target:
            raise RuntimeError("Tidak dapat menemukan frame kuis.")
        await target.evaluate(self.som_script)
        await target.evaluate("window.injectSoM()")
        await asyncio.sleep(duration_seconds)
        await target.evaluate("window.removeSoM(true)")

    async def click_element(self, element_id: int, elements_map: List[Dict[str, Any]], delay: float = 0.05) -> bool:
        if not self.page:
            return False

        target_frame = self.active_frame or await self.find_best_quiz_frame()
        if not target_frame:
            return False

        # METODE UTAMA: Playwright Frame Locator langsung pada target frame
        try:
            locator = target_frame.locator(f'[data-som-id="{element_id}"]')
            if await locator.count() > 0:
                await locator.first.click(timeout=1500, no_wait_after=True)
                if delay > 0:
                    await asyncio.sleep(delay)
                return True
        except Exception:
            pass

        # METODE FALLBACK: Koordinat mouse absolut
        target_el = next((e for e in elements_map if e["id"] == element_id), None)
        if target_el:
            rect = target_el.get("rect", {})
            x = rect.get("x", 0) + (rect.get("width", 0) / 2)
            y = rect.get("y", 0) + (rect.get("height", 0) / 2)
            try:
                await self.page.mouse.click(x, y)
                if delay > 0:
                    await asyncio.sleep(delay)
                return True
            except Exception:
                pass

        return False

    async def get_question_hash(self) -> str:
        if not self.page:
            return ""
        try:
            target = self.active_frame or await self.find_best_quiz_frame()
            if not target:
                return ""
            text = await target.evaluate("() => (document.body.innerText || '').replace(/\\s+/g, ' ')")
            return hashlib.sha256(text[:1000].encode("utf-8")).hexdigest()
        except Exception:
            return ""

    async def close(self):
        if self.context:
            try:
                await self.context.close()
            except Exception:
                pass
        if self.browser:
            try:
                await self.browser.close()
            except Exception:
                pass
        if self.playwright:
            try:
                await self.playwright.stop()
            except Exception:
                pass
        self.context = None
        self.browser = None
        self.page = None
        self.active_frame = None
        self.playwright = None
