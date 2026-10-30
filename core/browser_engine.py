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
import http.client
from urllib.parse import urlparse
from typing import Optional, List, Dict, Any, Tuple, Union
from PIL import Image
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Frame

logger = logging.getLogger("SeeNOW.Browser")

def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_path, relative_path)

def format_endpoint_url(host: str, port: int) -> str:
    h = f"[{host}]" if ":" in host and not host.startswith("[") else host
    return f"http://{h}:{port}"

def parse_host_port(cdp_url: str) -> Tuple[str, int]:
    try:
        parsed = urlparse(cdp_url)
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or 9222
        return host, port
    except Exception:
        return "127.0.0.1", 9222

def is_cdp_endpoint_ready(port: int, host: str = "127.0.0.1", timeout: float = 0.6) -> bool:
    try:
        conn = http.client.HTTPConnection(host, port, timeout=timeout)
        conn.request("GET", "/json/version", headers={"User-Agent": "SeeNOW-CDP-Probe"})
        resp = conn.getresponse()
        status = resp.status
        conn.close()
        return status == 200
    except Exception:
        return False

def cleanup_profile_locks(profile_dir: str):
    if not os.path.isdir(profile_dir):
        return
    for lock in ("SingletonLock", "SingletonCookie", "SingletonSocket", "lockfile"):
        p = os.path.join(profile_dir, lock)
        if os.path.exists(p):
            try:
                os.remove(p)
                logger.info(f"Berhasil membersihkan file lock profil lama: {lock}")
            except Exception:
                pass

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
        cleanup_profile_locks(profile_dir)

        cmd = [
            exe,
            f"--remote-debugging-port={cdp_port}",
            f"--user-data-dir={profile_dir}",
            "--no-first-run",
            "--no-default-browser-check"
        ]

        try:
            self.chrome_process = subprocess.Popen(cmd)
            time.sleep(0.8)
            logger.info(f"Browser berhasil diluncurkan dengan port {cdp_port}")
            return True
        except Exception as e:
            logger.error(f"Gagal meluncurkan browser: {e}")
            return False

    async def ensure_browser_running(self, cdp_url: str = "http://localhost:9222") -> str:
        host, port = parse_host_port(cdp_url)

        # 1. Cek apakah endpoint sudah siap di host:port
        if is_cdp_endpoint_ready(port, host):
            logger.info(f"Endpoint browser CDP aktif di {host}:{port}")
            return format_endpoint_url(host, port)

        # 2. Coba luncurkan browser di port utama
        logger.info(f"Port {port} belum merespons. Meluncurkan browser otomatis...")
        if self.launch_debug_browser(cdp_port=port):
            for _ in range(12):
                await asyncio.sleep(0.25)
                if is_cdp_endpoint_ready(port, host):
                    logger.info(f"Browser siap di {host}:{port}")
                    return format_endpoint_url(host, port)

        # 3. Fallback Port Discovery (9223, 9224) jika port 9222 macet atau bentrok
        candidates = [9223, 9224] if port == 9222 else [9222, 9223]
        for f_port in candidates:
            if is_cdp_endpoint_ready(f_port, host):
                logger.info(f"Ditemukan browser aktif di fallback port {f_port}")
                new_url = format_endpoint_url(host, f_port)
                if self.config:
                    self.config.set("browser_cdp_url", new_url)
                return new_url

            logger.info(f"Mencoba meluncurkan browser di fallback port {f_port}...")
            if self.launch_debug_browser(cdp_port=f_port):
                for _ in range(8):
                    await asyncio.sleep(0.25)
                    if is_cdp_endpoint_ready(f_port, host):
                        logger.info(f"Browser siap di fallback port {f_port}")
                        new_url = format_endpoint_url(host, f_port)
                        if self.config:
                            self.config.set("browser_cdp_url", new_url)
                        return new_url

        raise RuntimeError(
            f"CDP Refused: Tidak dapat terhubung ke browser di port {port}. "
            "Harap tutup semua jendela Chrome di Task Manager lalu klik Attach kembali."
        )

    async def connect_cdp(self, cdp_url: str = "http://localhost:9222") -> Page:
        effective_url = await self.ensure_browser_running(cdp_url)

        if not self.playwright:
            self.playwright = await async_playwright().start()

        try:
            self.browser = await self.playwright.chromium.connect_over_cdp(effective_url)
        except Exception as e:
            logger.error(f"Gagal connect_over_cdp ke {effective_url}: {e}")
            raise RuntimeError(
                f"CDP Refused: Gagal terhubung ke {effective_url}. "
                "Tutup semua jendela Chrome lalu klik Attach kembali."
            ) from e

        contexts = self.browser.contexts
        if contexts:
            self.context = contexts[0]
        else:
            self.context = await self.browser.new_context()

        pages = self.context.pages
        if pages:
            best = pages[0]
            # Prioritaskan tab yang URL-nya mengandung examContent atau kuis aktif
            for p in pages:
                url = p.url.lower()
                if "examcontent" in url or "quiz" in url or "assessment" in url:
                    best = p
                    break
                elif not url.startswith("chrome://") and not url.startswith("about:blank") and not url.startswith("edge://"):
                    best = p
            self.page = best
        else:
            self.page = await self.context.new_page()

        if self.config and self.config.get("prevent_blur_detection", True):
            await self.apply_anti_blur_stealth(self.page)

        # Pasang listener otomatis bila ada tab popup lembar ujian terbuka
        async def _on_new_page(new_p: Page):
            await asyncio.sleep(0.4)
            url_lower = new_p.url.lower()
            if "examcontent" in url_lower or "exam" in url_lower or "quiz" in url_lower:
                self.page = new_p
                self.active_frame = self.page
                logger.info(f"Otomatis mengunci ke tab lembar ujian baru: {new_p.url}")
                if self.config and self.config.get("prevent_blur_detection", True):
                    await self.apply_anti_blur_stealth(self.page)

        try:
            self.context.on("page", lambda p: asyncio.create_task(_on_new_page(p)))
        except Exception:
            pass

        return self.page

    async def list_open_tabs(self) -> List[Dict[str, Any]]:
        if not self.context:
            return []
        result = []
        for i, p in enumerate(self.context.pages):
            if p.is_closed():
                continue
            try:
                title = await p.title()
            except Exception:
                title = "Untitled Tab"
            url = p.url
            result.append({
                "index": i,
                "title": title[:35] if title else "Untitled",
                "url": url,
                "is_active": (p == self.page)
            })
        return result

    async def select_tab(self, index: int) -> bool:
        if not self.context:
            return False
        pages = self.context.pages
        if 0 <= index < len(pages):
            target_page = pages[index]
            if not target_page.is_closed():
                self.page = target_page
                self.active_frame = self.page
                try:
                    await self.page.bring_to_front()
                except Exception:
                    pass
                if self.config and self.config.get("prevent_blur_detection", True):
                    await self.apply_anti_blur_stealth(self.page)
                logger.info(f"Berhasil mengunci agen ke tab #{index}: {target_page.url}")
                return True
        return False

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

    async def apply_anti_blur_stealth(self, target: Optional[Page] = None):
        stealth_js = """
        (() => {
            try {
                // 1. Force Page Visibility API
                const defineVis = (targetObj) => {
                    try {
                        Object.defineProperty(targetObj, 'visibilityState', { get: () => 'visible', configurable: true });
                        Object.defineProperty(targetObj, 'hidden', { get: () => false, configurable: true });
                        Object.defineProperty(targetObj, 'webkitVisibilityState', { get: () => 'visible', configurable: true });
                        Object.defineProperty(targetObj, 'webkitHidden', { get: () => false, configurable: true });
                    } catch(e) {}
                };
                defineVis(document);
                if (typeof Document !== 'undefined' && Document.prototype) {
                    defineVis(Document.prototype);
                }

                // 2. Force hasFocus
                if (typeof Document !== 'undefined' && Document.prototype) {
                    Document.prototype.hasFocus = () => true;
                }
                document.hasFocus = () => true;

                // 3. Nullify inline event handlers
                window.onblur = null;
                window.onfocus = null;
                document.onvisibilitychange = null;
                window.onpagehide = null;

                // 4. Trap and discard all blur, focusout, visibilitychange, pagehide events
                const blockEvent = (e) => {
                    e.stopImmediatePropagation();
                    e.stopPropagation();
                };

                const targetEvents = ['blur', 'focusout', 'visibilitychange', 'webkitvisibilitychange', 'pagehide'];
                targetEvents.forEach(evt => {
                    window.addEventListener(evt, blockEvent, true);
                    document.addEventListener(evt, blockEvent, true);
                });

                // 5. Intercept window.open to prevent duplicate/blank tab spawning on exam portals
                const origOpen = window.open;
                window.open = function(url, target, features) {
                    if (url && typeof url === 'string') {
                        window.location.href = url;
                        return window;
                    }
                    return origOpen ? origOpen.apply(this, arguments) : null;
                };

                // 6. Rewrite target="_blank" links
                document.addEventListener('click', (e) => {
                    const a = e.target && e.target.closest ? e.target.closest('a') : null;
                    if (a && a.target === '_blank') {
                        a.target = '_self';
                    }
                }, true);

                // 7. Bypass anti-copy & text-selection locks (user-select: none, oncopy, onselectstart)
                try {
                    if (!document.getElementById('seenow-unlock-select')) {
                        const unlockStyle = document.createElement('style');
                        unlockStyle.id = 'seenow-unlock-select';
                        unlockStyle.innerHTML = `
                            *, *:before, *:after {
                                -webkit-user-select: text !important;
                                -moz-user-select: text !important;
                                -ms-user-select: text !important;
                                user-select: text !important;
                            }
                        `;
                        (document.head || document.documentElement).appendChild(unlockStyle);
                    }
                } catch(e) {}

                const unlockEvents = ['copy', 'cut', 'selectstart', 'contextmenu', 'dragstart'];
                unlockEvents.forEach(evt => {
                    window.addEventListener(evt, e => e.stopImmediatePropagation(), true);
                    document.addEventListener(evt, e => e.stopImmediatePropagation(), true);
                });
            } catch(err) {}
        })();
        """
        # Inject at Context level so all pages, popups, and iframes inherit stealth
        if self.context:
            try:
                await self.context.add_init_script(stealth_js)
            except Exception as e:
                logger.debug(f"Context add_init_script note: {e}")

        # Also inject immediately into target page or self.page
        p = target or self.page
        if p and not p.is_closed():
            try:
                await p.evaluate(stealth_js)
            except Exception as e:
                logger.debug(f"Page evaluate stealth note: {e}")

    async def auto_focus_exam_tab(self) -> Optional[Page]:
        if not self.context:
            return None
        pages = self.context.pages
        for p in pages:
            if p.is_closed():
                continue
            url = p.url.lower()
            if "examcontent" in url or "quiz" in url or "assessment" in url:
                if self.page != p:
                    self.page = p
                    self.active_frame = self.page
                    try:
                        await self.page.bring_to_front()
                    except Exception:
                        pass
                    if self.config and self.config.get("prevent_blur_detection", True):
                        await self.apply_anti_blur_stealth(self.page)
                    logger.info(f"Otomatis mengunci ke tab lembar ujian: {p.url}")
                return self.page
        return self.page

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
                    () => document.querySelectorAll('input[type="radio"], input[type="checkbox"], [role="radio"], [role="checkbox"], .option, .option-list-item, .quiz-option, .choice-item').length
                """)
                if count > max_inputs:
                    max_inputs = count
                    best_frame = f
            except Exception:
                continue

        self.active_frame = best_frame
        return best_frame

    async def capture_som_state(self) -> Tuple[str, List[Dict[str, Any]], str]:
        if not self.page or self.page.is_closed():
            raise RuntimeError("Browser belum terhubung atau tab telah ditutup.")

        target = await self.find_best_quiz_frame()
        if not target:
            raise RuntimeError("Tidak dapat menemukan frame kuis.")

        # Single roundtrip: inject script + execute injectSoM atomically & decode any diagram images
        try:
            elements = await target.evaluate(f"""
                {self.som_script}
                // Pastikan gambar topologi/diagram kuis selesai di-render
                try {{
                    const imgs = Array.from(document.images || []);
                    for (const img of imgs) {{
                        if (img.decode && img.complete) {{
                            img.decode().catch(() => {{}});
                        }}
                    }}
                }} catch(e) {{}}
                window.injectSoM();
            """)
        except Exception as e:
            logger.warning(f"Gagal menyuntikkan SoM: {e}")
            raise RuntimeError(f"Gagal menyuntikkan SoM pada halaman: {e}")

        # Ambil screenshot JPEG 60%
        try:
            raw_bytes = await self.page.screenshot(type="jpeg", quality=60, full_page=False)
        except Exception as e:
            logger.warning(f"Gagal mengambil screenshot: {e}")
            raise RuntimeError(f"Gagal mengambil screenshot halaman: {e}")

        # Kompresi ultra-cepat: Batasi lebar maksimal 960px menggunakan Bilinear (<5ms vs 100ms Lanczos)
        try:
            with Image.open(io.BytesIO(raw_bytes)) as pil_img:
                w, h = pil_img.size
                if w > 960:
                    new_w = 960
                    new_h = int(h * (960 / w))
                    resized_img = pil_img.resize((new_w, new_h), Image.Resampling.BILINEAR)
                    buf = io.BytesIO()
                    resized_img.save(buf, format="JPEG", quality=60, optimize=True)
                    raw_bytes = buf.getvalue()
        except Exception:
            pass

        screenshot_b64 = base64.b64encode(raw_bytes).decode("utf-8")

        # Single roundtrip: Hapus overlay visual dan ambil teks pertanyaan DOM bersamaan
        dom_question_text = ""
        try:
            dom_question_text = await target.evaluate("""() => {
                try { window.removeSoM(false); } catch(e) {}
                const qEl = document.querySelector('.editor-content, .subject-desc, .subject-title, .question-title, .exam-content-title, .subject-content');
                return qEl ? qEl.innerText.replace(/\\s+/g, ' ').trim() : '';
            }""")
        except Exception:
            pass

        summary_lines = []
        if dom_question_text:
            summary_lines.append(f"QUESTION TEXT (FROM DOM):\n\"{dom_question_text}\"\n")
            summary_lines.append("OPTIONS AND CONTROLS ON SCREEN:")
        for el in elements:
            checked_tag = " [ALREADY_CHECKED]" if el.get("is_checked") else ""
            summary_lines.append(
                f"[{el['id']}] Tag: <{el['tag']}> Type: '{el['type']}'{checked_tag} Text: \"{el['text']}\""
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

    JS_EXTRACT_QUESTION = """() => {
        const bodyText = document.body.innerText || '';

        // 1. Nomor soal & total
        let current = null;
        let total = null;
        const m = bodyText.match(/Question\\s+(\\d+)\\s*\\/\\s*(\\d+)/i);
        if (m) {
            current = parseInt(m[1]);
            total = parseInt(m[2]);
        } else {
            const m2 = bodyText.match(/\\b(\\d+)[、\\.]\\s*[A-Z]/);
            if (m2) current = parseInt(m2[1]);
        }

        // 2. Teks stem pertanyaan
        // Prioritas 1: Selector kelas pertanyaan spesifik
        const stemSelectors = [
            '.subject-desc', '.question-stem', '.subject-stem',
            '.question-title', '.subject_content', '.subject-item-title',
            '.exam-question-title', '.title-box', '.q-title', '.stem',
            '.question-box .title', '.subject-item .title', '.exam-subject-title'
        ];
        for (const sel of stemSelectors) {
            const el = document.querySelector(sel);
            if (el && (el.innerText || '').trim().length >= 8) {
                return { current, total, text: (el.innerText || '').trim().replace(/\\s+/g, ' ') };
            }
        }

        // Prioritas 2: Cari elemen teks sebelum opsi pertama kuis
        const firstOpt = document.querySelector(
            '.kltCourse-radio-wrapper, .kltCourse-checkbox-wrapper, .option-list-item, .quiz-option, .choice-item, label.el-radio, label.el-checkbox, [role="radio"], [role="checkbox"]'
        );
        if (firstOpt) {
            let p = firstOpt.parentElement;
            while (p && p !== document.body) {
                for (let i = 0; i < p.children.length; i++) {
                    const child = p.children[i];
                    if (child.contains(firstOpt)) break;
                    const txt = (child.innerText || '').trim().replace(/\\s+/g, ' ');
                    if (txt.length >= 8 && !/^(Remaining|Time|Score|Answered|Skor|Waktu)/i.test(txt)) {
                        return { current, total, text: txt };
                    }
                }
                p = p.parentElement;
            }
        }

        // Prioritas 3: Regex berbasis teks pertanyaan di body (menangkap 'Question X / Y ... [soal] ...')
        const qMatch = bodyText.match(/(?:Question\\s+\\d+\\s*\\/\\s*\\d+|\\b\\d+[、\\.]\\s*[A-Z])[\\s\\S]{10,600}/i);
        if (qMatch) {
            const cleaned = qMatch[0]
                .replace(/\\b\\d{1,2}:\\d{2}(:\\d{2})?\\b/g, '')
                .replace(/\\b(Answered|Score|Time|Remaining|Terjawab|Skor|Waktu)\\s*[:：]?\\s*\\d+(\\/\\d+)?/gi, '')
                .replace(/\\b(Saved|Saving|Tersimpan|Menyimpan)\\b/gi, '')
                .replace(/\\s+/g, ' ')
                .trim();
            return { current, total, text: cleaned };
        }

        // Prioritas 4: Container umum jika ada
        const qContainer = document.querySelector('.subject-item, .question-item, .exam-subject, .exam-question, .subject-box, .test-paper, #questionContainer');
        if (qContainer && (qContainer.innerText || '').trim().length >= 15) {
            const cleaned = (qContainer.innerText || '')
                .replace(/\\b\\d{1,2}:\\d{2}(:\\d{2})?\\b/g, '')
                .replace(/\\b(Answered|Score|Time|Remaining|Terjawab|Skor|Waktu)\\s*[:：]?\\s*\\d+(\\/\\d+)?/gi, '')
                .replace(/\\s+/g, ' ')
                .trim();
            return { current, total, text: cleaned.slice(0, 500) };
        }

        return { current, total, text: "" };
    }"""

    async def get_question_info(self) -> Dict[str, Any]:
        if not self.page:
            return {"current": None, "total": None, "text": ""}
        try:
            target = self.active_frame or await self.find_best_quiz_frame()
            if not target:
                return {"current": None, "total": None, "text": ""}
            res = await target.evaluate(self.JS_EXTRACT_QUESTION)
            return {
                "current": res.get("current"),
                "total": res.get("total"),
                "text": res.get("text", "")
            }
        except Exception:
            return {"current": None, "total": None, "text": ""}

    async def get_question_hash(self) -> str:
        if not self.page:
            return ""
        try:
            target = self.active_frame or await self.find_best_quiz_frame()
            if not target:
                return ""
            res = await target.evaluate(self.JS_EXTRACT_QUESTION)
            cur_num = res.get("current")
            text = res.get("text", "")
            ident = f"Q{cur_num}_{text}" if cur_num is not None else text
            return hashlib.sha256(ident.encode("utf-8")).hexdigest() if ident else ""
        except Exception:
            return ""

    async def check_question_status(self, pre_num: Optional[int], pre_hash: str) -> Dict[str, Any]:
        """
        Pemeriksaan status perubahan soal dalam 1 roundtrip evaluate yang super cepat (<10ms).
        Menggunakan logika ekstraksi identik dengan get_question_hash() untuk mencegah false positive.
        """
        if not self.page:
            return {"changed": False, "current": pre_num, "hash": pre_hash}
        try:
            target = self.active_frame or await self.find_best_quiz_frame()
            if not target:
                return {"changed": False, "current": pre_num, "hash": pre_hash}

            res = await target.evaluate(self.JS_EXTRACT_QUESTION)
            cur_num = res.get("current")
            text = res.get("text", "")
            ident = f"Q{cur_num}_{text}" if cur_num is not None else text
            cur_hash = hashlib.sha256(ident.encode("utf-8")).hexdigest() if ident else ""

            # Evaluasi perubahan soal secara presisi dan anti-false-positive:
            if cur_num is not None and pre_num is not None:
                # Jika kedua nomor soal terdeteksi:
                # HANYA nomor soal yang bertambah (cur_num > pre_num) yang valid sebagai perpindahan soal!
                # cur_num == pre_num (#16 -> #16) adalah false positive dan DITOLAK!
                changed = bool(cur_num > pre_num)
            elif pre_hash and cur_hash:
                # Jika nomor soal tidak tersedia di DOM, gunakan sidik jari hash teks pertanyaan
                changed = bool(cur_hash != pre_hash)
            else:
                changed = False

            return {
                "changed": changed,
                "current": cur_num,
                "hash": cur_hash
            }
        except Exception:
            return {"changed": False, "current": pre_num, "hash": pre_hash}

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
