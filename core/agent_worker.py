# core/agent_worker.py
import time
import asyncio
import logging
import threading
from typing import Callable, Optional, Dict, Any, List
from core.browser_engine import BrowserEngine
from core.llm_router import LLMRouterClient
from core.cache_manager import QuestionCacheManager, compute_question_cache_key
from core.quiz_notary import QuizNotary

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
        self.notary = QuizNotary()
        self.question_counter = 0

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
            self.status_cb("Connecting...", "Memeriksa & menghubungkan ke browser CDP...")
            try:
                cdp_url = self.config.get("browser_cdp_url", "http://localhost:9222")
                await self.browser_engine.connect_cdp(cdp_url)
                self.status_cb("Connected", "Terhubung ke browser kuis.")
                return True
            except Exception as e:
                err_str = str(e)
                if "CDP Refused" in err_str:
                    diag = "CDP Refused: Tutup semua jendela Chrome lalu klik Attach kembali."
                elif "Timeout" in err_str:
                    diag = "CDP Timeout: Browser sibuk atau terblokir."
                else:
                    diag = f"Gagal CDP: {err_str[:40]}"
                self.status_cb("Error", diag)
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

        # 1. Otomatis fokus & kunci ke tab ujian jika ada tab examContent terbuka di background
        await self.browser_engine.auto_focus_exam_tab()

        current_url = (self.browser_engine.page.url if self.browser_engine.page else "").lower()

        # Deteksi halaman hasil ujian (examResult)
        if "examresult" in current_url:
            self.status_cb("Exam Ended", "Ujian selesai. Skor/Hasil ujian terdeteksi.")
            logger.info("Mendeteksi halaman hasil ujian (examResult). Auto-loop dihentikan.")
            if self.is_running:
                self.stop_loop()
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

        # Deteksi jika saat ini masih di halaman pengantar ujian (examInfo)
        if "examinfo" in current_url:
            start_btn = next(
                (el for el in elements if any(kw in (el.get("text") or "").lower() for kw in ("start answering", "start exam", "mulai ujian", "mulai kerjakan", "start"))),
                None
            )
            if start_btn:
                self.status_cb("Starting Exam...", "Mendeteksi halaman pengantar. Memulai ujian...")
                logger.info(f"Mengklik tombol Mulai Ujian [{start_btn['id']}]: {start_btn.get('text')}")
                await self.browser_engine.click_element(start_btn["id"], elements, delay=0.1)

                # Tunggu navigasi in-place ke examContent
                for _ in range(16):
                    await asyncio.sleep(0.25)
                    await self.browser_engine.auto_focus_exam_tab()
                    c_url = (self.browser_engine.page.url if self.browser_engine.page else "").lower()
                    if "examcontent" in c_url:
                        self.status_cb("Exam Loaded", "Berhasil masuk ke lembar ujian aktif.")
                        logger.info("Berhasil masuk ke lembar ujian aktif (examContent).")
                        await asyncio.sleep(0.4)
                        return True

                self.status_cb("Waiting...", "Menunggu lembar ujian dimuat...")
                return False
            else:
                self.status_cb("Non-Quiz Tab", "Bukan halaman soal. Harap buka tab ujian.")
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
                analysis = self.llm_client.analyze_quiz(screenshot_b64, summary, elements=elements)
                if enable_cache:
                    self.cache_manager.put(cache_key, analysis)
            except Exception as e:
                self.status_cb("Error", f"Gagal analisis LLM: {e}")
                return False

        analysis["screenshot_b64"] = screenshot_b64
        self.result_cb(analysis)

        # Catat hasil ke QuizNotary
        self.question_counter += 1
        self.notary.log_question_answer(
            question_number=self.question_counter,
            question_summary=analysis.get("question_summary", ""),
            question_type=analysis.get("question_type", "unknown"),
            reasoning=analysis.get("reasoning", ""),
            selected_ids=analysis.get("correct_option_ids", []),
            selected_texts=analysis.get("correct_option_texts", []),
            confidence=analysis.get("confidence_score", 1.0)
        )

        exec_mode = self.config.get("execution_mode", "auto_click_answer_only")

        if exec_mode == "read_only":
            duration = round(time.time() - t_start, 2)
            self.status_cb("Idle", f"Selesai dalam {duration}s (Read-Only).")
            return not analysis.get("is_final_submit", False)

        # 1. Catat informasi nomor soal dan sidik jari sebelum aksi
        q_info = await self.browser_engine.get_question_info()
        cur_num = q_info.get("current")
        total_num = q_info.get("total")
        pre_answer_hash = await self.browser_engine.get_question_hash()

        # Deteksi apakah ini soal terakhir dari DOM atau analisis LLM
        is_final = analysis.get("is_final_submit", False) or bool(cur_num and total_num and cur_num >= total_num)
        raw_next_id = analysis.get("next_button_id")

        # Validasi bahwa tombol next yang dipilih adalah tombol maju (BUKAN prev / return)
        def is_forward_button(el_id: Optional[int]) -> bool:
            if el_id is None:
                return False
            el = next((e for e in elements if e["id"] == el_id), None)
            if not el:
                return False
            t = (el.get("text") or "").lower()
            if any(bw in t for bw in ("prev", "previous", "kembali", "sebelumnya", "back", "return")):
                return False
            return True

        next_id = raw_next_id if is_forward_button(raw_next_id) else None
        if next_id is None:
            fwd_el = next((el for el in elements if (el.get("text") or "").strip().lower() in ("next", "selanjutnya", "lanjut")), None)
            if fwd_el:
                next_id = fwd_el["id"]

        # 2. Periksa status tercentang (Pre-Checked / Already-Filled) pada elemen saat ini
        desired_ids = analysis.get("correct_option_ids", [])
        q_type = analysis.get("question_type", "single_choice")
        currently_checked_ids = [el["id"] for el in elements if el.get("is_checked", False)]

        # Validasi apakah jawaban yang ada di layar sudah 100% benar
        already_correct = False
        if desired_ids:
            if q_type in ("single_choice", "true_false"):
                # Pada radio button, jika salah satu yang tercentang sama dengan target jawaban
                if any(cid in desired_ids for cid in currently_checked_ids):
                    already_correct = True
                    logger.info(f"Pre-check Valid: Soal #{cur_num or '?'} radio [{currently_checked_ids}] sudah benar ({desired_ids}). Melewati klik opsi.")
                    self.status_cb("Verified", f"Soal #{cur_num or '?'} sudah terisi benar.")
            else:
                # Pada multi-choice, himpunan opsi tercentang harus 100% sama dengan target
                if set(currently_checked_ids) == set(desired_ids):
                    already_correct = True
                    logger.info(f"Pre-check Valid: Soal #{cur_num or '?'} multi-choice [{currently_checked_ids}] sudah 100% cocok. Melewati klik opsi.")
                    self.status_cb("Verified", f"Soal #{cur_num or '?'} opsi [{desired_ids}] sudah terisi benar.")

        # 3. Rekonsiliasi & Eksekusi Opsi jika belum benar
        action_performed = False
        if not already_correct:
            if desired_ids:
                if q_type == "multi_choice":
                    # Multi-answer (checkbox):
                    # - Uncheck opsi salah yang tercentang
                    wrong_checked = set(currently_checked_ids) - set(desired_ids)
                    for opt_id in wrong_checked:
                        logger.info(f"Membatalkan centang opsi yang salah [{opt_id}]...")
                        await self.browser_engine.click_element(opt_id, elements, delay=0.08)
                        action_performed = True

                    # - Check opsi benar yang belum tercentang
                    missing_options = set(desired_ids) - set(currently_checked_ids)
                    for opt_id in missing_options:
                        logger.info(f"Mencentang opsi yang benar [{opt_id}]...")
                        await self.browser_engine.click_element(opt_id, elements, delay=0.08)
                        action_performed = True
                else:
                    # Single-choice atau True/False (radio): Cukup klik opsi yang benar
                    self.status_cb("Clicking...", f"Memilih opsi ID: {desired_ids}")
                    for opt_id in desired_ids:
                        await self.browser_engine.click_element(opt_id, elements, delay=0.06)
                        action_performed = True
            else:
                # Jika tidak ada opsi terpilih dan tidak ada elemen interaktif pilihan ganda
                has_options = any(
                    el.get("tag") == "input" or el.get("role") in ("radio", "checkbox") or "option" in el.get("text", "").lower()
                    for el in elements
                )
                if not has_options:
                    self.status_cb("Non-Quiz Tab", "Bukan halaman soal. Beralih ke tab lembar ujian.")
                    logger.warning("Tidak ada elemen pilihan ganda di tab ini. Auto-loop dijeda agar tidak salah klik.")
                    return False

        duration = round(time.time() - t_start, 2)

        # 4. KASUS KHUSUS SOAL TERAKHIR (Submit Page)
        if is_final:
            if action_performed:
                await asyncio.sleep(0.3)

            auto_submit = self.config.get("auto_submit_final", False)
            submit_target_id = raw_next_id if raw_next_id and is_forward_button(raw_next_id) else None
            if not submit_target_id:
                submit_el = next((el for el in elements if any(w in (el.get("text") or "").lower() for w in ("submit", "kirim", "finish", "selesai"))), None)
                if submit_el:
                    submit_target_id = submit_el["id"]

            if auto_submit and submit_target_id:
                logger.info(f"Soal terakhir #{cur_num or 'Final'}: Mengklik tombol submit [{submit_target_id}]...")
                await self.browser_engine.click_element(submit_target_id, elements, delay=0.1)
                self.status_cb("Completed", "Ujian disubmit otomatis.")
            else:
                self.status_cb("Quiz Finished", f"Soal akhir #{cur_num or 'Final'} selesai ({duration}s). Dijeda untuk review.")

            self.stop_loop()
            return False

        # 5. ATURAN AUTO-ADVANCE & NAVIGASI
        # Cek apakah platform Huawei beralih otomatis (hanya jika opsi single/true_false baru diklik)
        auto_advanced = False
        if action_performed and q_type in ("single_choice", "true_false"):
            self.status_cb("Auto-Advance", f"Menunggu auto-advance Soal #{cur_num or '?'}...")
            for _ in range(6):
                await asyncio.sleep(0.05)
                chk = await self.browser_engine.check_question_status(cur_num, pre_answer_hash)
                if chk.get("changed"):
                    auto_advanced = True
                    logger.info(f"Platform auto-advanced: #{cur_num} -> #{chk.get('current')}.")
                    break

        if auto_advanced:
            await asyncio.sleep(0.06)
            if exec_mode == "auto_click_and_next":
                self.status_cb("Idle", f"Soal #{cur_num or '?'} selesai via Auto-Advance ({duration}s).")
                return True
            else:
                self.status_cb("Waiting Next", f"Jawaban dicentang ({duration}s).")
                return False

        # 6. Mode Read/Answer Only
        if exec_mode == "auto_click_answer_only":
            self.status_cb("Waiting Next", f"Jawaban tervalidasi ({duration}s). Silakan klik Selanjutnya.")
            return False

        # 7. Eksekusi Tombol Next jika platform tidak auto-advance (atau multi-choice / pre-checked)
        if exec_mode == "auto_click_and_next":
            if next_id is not None:
                self.status_cb("Navigating...", f"Klik Next [{next_id}]...")
                clicked = await self.browser_engine.click_element(next_id, elements, delay=0.04)
                if not clicked:
                    logger.warning(f"Gagal mengklik tombol Next [{next_id}].")
                    return False

                # Polling pergantian soal kilat (50ms interval)
                changed = False
                for _ in range(35):
                    await asyncio.sleep(0.05)
                    chk = await self.browser_engine.check_question_status(cur_num, pre_answer_hash)
                    if chk.get("changed"):
                        changed = True
                        break

                if not changed:
                    logger.warning(f"Soal #{cur_num or '?'} belum berganti setelah klik Next. Dijeda untuk mencegah skip.")
                    return False

                duration = round(time.time() - t_start, 2)
                self.status_cb("Idle", f"Soal #{cur_num or '?'} selesai dalam {duration}s.")
                return True
            else:
                logger.warning(f"Tombol Next tidak ditemukan untuk Soal #{cur_num or '?'}.")
                return False

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
                await asyncio.sleep(0.5)
            else:
                consecutive_failures = 0
                step += 1
                cfg_delay = float(self.config.get("action_delay", 0.3))
                await asyncio.sleep(max(0.1, cfg_delay))

        self.is_running = False
        self.status_cb("Idle", "Auto-Loop selesai.")

    def stop_loop(self):
        self.is_running = False
        self.status_cb("Stopping...", "Menghentikan auto-loop...")
