# core/agent_worker.py
import time
import asyncio
import logging
import threading
from typing import Callable, Optional, Dict, Any, List
from core.browser_engine import BrowserEngine
from core.llm_router import LLMRouterClient
from core.cache_manager import QuestionCacheManager, compute_question_cache_key

logger = logging.getLogger("SeeNOW.Worker")

class AgentWorker(threading.Thread):
    def __init__(
        self,
        config_manager,
        status_callback: Callable[[str, str], None],
        result_callback: Callable[[Dict[str, Any]], None],
        tabs_callback: Optional[Callable[[List[Dict[str, Any]]], None]] = None
    ):
        super().__init__(daemon=True)
        self.config = config_manager
        self.status_cb = status_callback
        self.result_cb = result_callback
        self.tabs_cb = tabs_callback

        self.browser_engine = BrowserEngine(self.config)
        self.llm_client = LLMRouterClient(self.config)
        self.cache_manager = QuestionCacheManager()

        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.is_running = False
        self.task_queue: Optional[asyncio.Queue[Any]] = None
        self.ready_event = threading.Event()

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.task_queue = asyncio.Queue()
        self.ready_event.set()
        self.loop.run_until_complete(self._worker_loop())

    async def _worker_loop(self):
        if not self.task_queue:
            return
        while True:
            cmd, args = await self.task_queue.get()
            if cmd == "exit":
                break
            try:
                if cmd == "solve_once":
                    await self._do_solve_once()
                elif cmd == "auto_loop":
                    await self._do_auto_loop()
                elif cmd == "test_overlay":
                    await self._do_test_overlay()
                elif cmd == "connect_browser":
                    await self._do_connect_browser()
                elif cmd == "list_tabs":
                    await self._do_list_tabs()
                elif cmd == "select_tab":
                    await self._do_select_tab(args)
            except Exception as e:
                logger.error(f"Error pada loop worker {cmd}: {e}", exc_info=True)
                self.status_cb("Error", f"Error: {e}")
            finally:
                if self.task_queue:
                    self.task_queue.task_done()

    def dispatch(self, cmd: str, args: Any = None):
        self.ready_event.wait()
        if self.loop and self.task_queue:
            self.loop.call_soon_threadsafe(self.task_queue.put_nowait, (cmd, args))

    async def _ensure_connected(self) -> bool:
        if not await self.browser_engine.is_connection_alive():
            self.status_cb("Connecting...", "Menghubungkan ke browser via CDP...")
            try:
                cdp_url = self.config.get("browser_cdp_url", "http://localhost:9222")
                await self.browser_engine.connect_cdp(cdp_url)
                self.status_cb("Connected", "Terhubung ke browser kuis.")
                return True
            except Exception as e:
                self.status_cb("Error", f"Gagal CDP: {e}")
                return False
        return True

    async def _do_connect_browser(self):
        if await self._ensure_connected():
            await self._do_list_tabs()

    async def _do_list_tabs(self):
        if not await self._ensure_connected():
            return
        tabs = await self.browser_engine.list_open_tabs()
        if self.tabs_cb:
            self.tabs_cb(tabs)

    async def _do_select_tab(self, index: int):
        if not await self._ensure_connected():
            return
        success = await self.browser_engine.select_tab(index)
        if success:
            self.status_cb("Tab Selected", f"Terkunci pada tab #{index}.")
            tabs = await self.browser_engine.list_open_tabs()
            if self.tabs_cb:
                self.tabs_cb(tabs)
        else:
            self.status_cb("Error", f"Gagal mengunci tab #{index}.")

    async def _do_test_overlay(self):
        if not await self._ensure_connected():
            return
        self.status_cb("Testing Overlay", "Menyuntikkan badge Set-of-Marks selama 3 detik...")
        try:
            await self.browser_engine.preview_som_overlay(3.0)
            self.status_cb("Idle", "Uji overlay selesai. Elemen berhasil dilabeli.")
        except Exception as e:
            self.status_cb("Error", f"Uji overlay gagal: {e}")

    async def _do_solve_once(self) -> bool:
        if not await self._ensure_connected():
            return False

        t_start = time.time()
        self.status_cb("Capturing...", "Memotret & memetakan DOM...")
        try:
            screenshot_b64, elements, summary = await self.browser_engine.capture_som_state()
        except Exception as e:
            self.status_cb("Error", f"Gagal membaca layar: {e}")
            return False

        if not elements:
            self.status_cb("Warning", "Tidak ada elemen interaktif terdeteksi di viewport.")
            return False

        # Smart Question Cache Check
        enable_cache = self.config.get("enable_question_cache", True)
        cache_hit = False
        analysis: Optional[Dict[str, Any]] = None
        current_opt_texts = [el.get("text", "") for el in elements if el.get("text")]
        page_hash_text = await self.browser_engine.get_question_hash()
        cache_key = compute_question_cache_key(page_hash_text, current_opt_texts)

        if enable_cache:
            cached_entry = self.cache_manager.get(cache_key)
            if cached_entry:
                cached_ids, cached_next = self.cache_manager.resolve_cached_options(cached_entry, elements)
                if cached_ids:
                    cache_hit = True
                    analysis = cached_entry.copy()
                    analysis["correct_option_ids"] = cached_ids
                    if cached_next is not None:
                        analysis["next_button_id"] = cached_next
                    t_cache = round(time.time() - t_start, 2)
                    self.status_cb("Cache Hit (0.02s)", f"Ditemukan di cache ({t_cache}s). Melewati panggilan LLM.")
                    logger.info(f"Cache Hit untuk soal [{analysis.get('question_summary', '')}].")

        if not cache_hit or analysis is None:
            self.status_cb("Thinking (9router)...", "Menganalisis soal...")
            try:
                analysis = self.llm_client.analyze_quiz(screenshot_b64, summary)
                if enable_cache:
                    self.cache_manager.put(cache_key, analysis)
            except Exception as e:
                self.status_cb("Error", f"Gagal analisis LLM: {e}")
                return False

        analysis["screenshot_b64"] = screenshot_b64
        self.result_cb(analysis)

        exec_mode = self.config.get("execution_mode", "auto_click_answer_only")

        if exec_mode == "read_only":
            duration = round(time.time() - t_start, 2)
            self.status_cb("Idle", f"Selesai dalam {duration}s (Read-Only).")
            return not analysis.get("is_final_submit", False)

        # Klik opsi jawaban
        correct_ids = analysis.get("correct_option_ids", [])
        if correct_ids:
            self.status_cb("Clicking...", f"Memilih opsi ID: {correct_ids}")
            for opt_id in correct_ids:
                await self.browser_engine.click_element(opt_id, elements, delay=0.06)

        is_final = analysis.get("is_final_submit", False)
        next_id = analysis.get("next_button_id")

        if is_final or (next_id is None):
            auto_submit = self.config.get("auto_submit_final", False)
            if auto_submit and next_id:
                await self.browser_engine.click_element(next_id, elements, delay=0.1)
                self.status_cb("Completed", "Ujian disubmit otomatis.")
            else:
                self.status_cb("Quiz Finished", "Mencapai soal akhir / submit. Dijeda.")
            return False

        if exec_mode == "auto_click_answer_only":
            duration = round(time.time() - t_start, 2)
            self.status_cb("Waiting Next", f"Jawaban dicentang ({duration}s). Silakan klik Selanjutnya.")
            return False

        if exec_mode == "auto_click_and_next":
            if next_id is not None:
                self.status_cb("Navigating...", f"Klik Next [{next_id}]...")
                old_hash = await self.browser_engine.get_question_hash()

                # Eksekusi klik tombol Next
                clicked = await self.browser_engine.click_element(next_id, elements, delay=0.08)
                if not clicked:
                    logger.warning(f"Gagal mengklik tombol Next [{next_id}].")
                    return False

                # Anti-Skipping & SPA Verification: Tunggu hingga hash teks soal berubah
                changed = False
                for _ in range(25):
                    await asyncio.sleep(0.1)
                    new_hash = await self.browser_engine.get_question_hash()
                    if new_hash and new_hash != old_hash:
                        changed = True
                        break

                if not changed:
                    logger.warning("Deteksi soal belum berganti setelah klik Next. Menunggu 0.5s ekstra.")
                    await asyncio.sleep(0.5)

                duration = round(time.time() - t_start, 2)
                self.status_cb("Idle", f"Soal selesai dalam {duration}s.")
                return True

        duration = round(time.time() - t_start, 2)
        self.status_cb("Idle", f"Selesai dalam {duration}s.")
        return True

    async def _do_auto_loop(self):
        self.is_running = True
        self.status_cb("Auto-Loop", "Siklus cepat dimulai...")

        step = 1
        consecutive_failures = 0

        while self.is_running:
            logger.info(f"Auto-Loop Step #{step}")
            success = await self._do_solve_once()

            if not self.is_running:
                break

            if not success:
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    logger.warning("3 kegagalan beruntun pada auto-loop. Menjeda loop untuk pencegahan skip.")
                    self.status_cb("Paused", "Auto-Loop dijeda demi keamanan (deteksi macet).")
                    break
                await asyncio.sleep(0.8)
            else:
                consecutive_failures = 0
                await asyncio.sleep(0.2)
                step += 1

        self.is_running = False
        self.status_cb("Idle", "Auto-Loop selesai.")

    def stop_loop(self):
        self.is_running = False
        self.status_cb("Stopping...", "Menghentikan auto-loop...")
