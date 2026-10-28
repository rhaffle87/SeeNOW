# gui/app_window.py
import logging
import customtkinter as ctk
from typing import Dict, Any
from core.config_manager import ConfigManager, validate_url
from core.agent_worker import AgentWorker
from gui.components import StatusBadge, AnswerCard

logger = logging.getLogger("SeeNOW.GUI")

try:
    import keyboard
except Exception:
    keyboard = None  # type: ignore

MODE_DESCRIPTIONS = {
    "auto_click_and_next": "⚡ Mencentang jawaban benar dan otomatis klik Selanjutnya hingga akhir.",
    "auto_click_answer_only": "🎯 Mencentang jawaban benar dan menunggu Anda meninjau sebelum klik manual.",
    "read_only": "👁️ Hanya menampilkan jawaban & bukti analitis tanpa menyentuh DOM browser."
}

MODE_LABELS = [
    ("⚡ Full Auto", "auto_click_and_next"),
    ("🎯 Click Only", "auto_click_answer_only"),
    ("👁️ Read-Only", "read_only")
]

class VisionQuizApp(ctk.CTk):
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config = config_manager

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("SeeNOW — Smart Exam Engine & Navigated Optical Workflow")
        self.geometry("540x700")
        self.minsize(480, 620)
        self.configure(fg_color="#090d16")

        # Inisialisasi background worker
        self.worker = AgentWorker(
            config_manager=self.config,
            status_callback=self._on_worker_status,
            result_callback=self._on_worker_result
        )
        self.worker.start()

        self._build_ui()
        self._setup_hotkeys()
        self._apply_always_on_top()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        # 1. Header Bar
        self.header_frame = ctk.CTkFrame(self, fg_color="#0f172a", corner_radius=0, height=50, border_width=1, border_color="#1e293b")
        self.header_frame.pack(side="top", fill="x")

        # Sisi Kiri: Brand + Badge Versi
        brand_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        brand_container.pack(side="left", padx=14, pady=8)

        lbl_brand = ctk.CTkLabel(
            brand_container,
            text="SeeNOW",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#f8fafc"
        )
        lbl_brand.pack(side="left")

        lbl_ver = ctk.CTkLabel(
            brand_container,
            text="v1.0.1",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#38bdf8",
            fg_color="#0369a1",
            corner_radius=4,
            padx=5,
            pady=1
        )
        lbl_ver.pack(side="left", padx=(8, 0))

        # Sisi Kanan: Always on Top Switch + Status Badge
        ctrl_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        ctrl_container.pack(side="right", padx=14, pady=8)

        self.cb_topmost = ctk.CTkCheckBox(
            ctrl_container,
            text="Pin Top",
            font=ctk.CTkFont(size=11),
            width=20,
            command=self._on_topmost_toggle
        )
        if self.config.get("always_on_top", True):
            self.cb_topmost.select()
        self.cb_topmost.pack(side="left", padx=(0, 10))

        self.status_badge = StatusBadge(ctrl_container)
        self.status_badge.pack(side="left")

        # 2. Tabview
        self.tabview = ctk.CTkTabview(
            self,
            fg_color="#0f172a",
            segmented_button_fg_color="#1e293b",
            segmented_button_selected_color="#2563eb",
            segmented_button_selected_hover_color="#1d4ed8"
        )
        self.tabview.pack(fill="both", expand=True, padx=12, pady=10)

        self.tab_hud = self.tabview.add("Live HUD")
        self.tab_settings = self.tabview.add("Settings & 9router")

        self._build_hud_tab()
        self._build_settings_tab()

        # 3. Bottom Bar
        self.bottom_bar = ctk.CTkFrame(self, fg_color="#090d16", height=26, corner_radius=0)
        self.bottom_bar.pack(side="bottom", fill="x", padx=14, pady=(0, 6))

        self.lbl_status_msg = ctk.CTkLabel(
            self.bottom_bar,
            text="Siap dijalankan.",
            font=ctk.CTkFont(size=11),
            text_color="#64748b",
            anchor="w"
        )
        self.lbl_status_msg.pack(side="left", fill="x", expand=True)

    def _build_hud_tab(self):
        # 1-Click Chrome Launcher
        self.btn_launch_chrome = ctk.CTkButton(
            self.tab_hud,
            text="🚀 Launch / Attach Chrome (CDP Port 9222)",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#0284c7",
            hover_color="#0369a1",
            height=38,
            corner_radius=8,
            command=self._launch_chrome
        )
        self.btn_launch_chrome.pack(fill="x", padx=10, pady=(8, 10))

        # Mode Selector Container
        mode_container = ctk.CTkFrame(self.tab_hud, fg_color="#111827", corner_radius=8, border_width=1, border_color="#1f2937")
        mode_container.pack(fill="x", padx=10, pady=(0, 10))

        lbl_mode_title = ctk.CTkLabel(mode_container, text="EXECUTION MODE", font=ctk.CTkFont(size=10, weight="bold"), text_color="#94a3b8")
        lbl_mode_title.pack(anchor="w", padx=12, pady=(8, 4))

        self.mode_var = ctk.StringVar(value=self.config.get("execution_mode", "auto_click_answer_only"))

        self.mode_segmented = ctk.CTkSegmentedButton(
            mode_container,
            values=[m[0] for m in MODE_LABELS],
            font=ctk.CTkFont(size=12, weight="bold"),
            selected_color="#2563eb",
            selected_hover_color="#1d4ed8",
            unselected_color="#1e293b",
            height=32,
            command=self._on_mode_change
        )
        # Tentukan opsi aktif
        initial_label = next((m[0] for m in MODE_LABELS if m[1] == self.mode_var.get()), MODE_LABELS[1][0])
        self.mode_segmented.set(initial_label)
        self.mode_segmented.pack(fill="x", padx=10, pady=(0, 4))

        # Dynamic mode caption
        self.lbl_mode_desc = ctk.CTkLabel(
            mode_container,
            text=MODE_DESCRIPTIONS.get(self.mode_var.get(), ""),
            font=ctk.CTkFont(size=11),
            text_color="#94a3b8",
            wraplength=480,
            justify="left"
        )
        self.lbl_mode_desc.pack(anchor="w", padx=12, pady=(0, 8))

        # Action Buttons Grid (4 Tombol Utama)
        btn_grid = ctk.CTkFrame(self.tab_hud, fg_color="transparent")
        btn_grid.pack(fill="x", padx=10, pady=2)
        btn_grid.grid_columnconfigure((0, 1), weight=1)

        self.btn_solve = ctk.CTkButton(
            btn_grid,
            text="Solve Once (Alt+S)",
            fg_color="#10b981",
            hover_color="#059669",
            height=38,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._solve_once
        )
        self.btn_solve.grid(row=0, column=0, padx=4, pady=4, sticky="ew")

        self.btn_loop = ctk.CTkButton(
            btn_grid,
            text="Start Auto-Loop (Alt+A)",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            height=38,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._start_loop
        )
        self.btn_loop.grid(row=0, column=1, padx=4, pady=4, sticky="ew")

        self.btn_overlay = ctk.CTkButton(
            btn_grid,
            text="Test Overlay (3s)",
            fg_color="#f59e0b",
            hover_color="#d97706",
            text_color="#000000",
            height=38,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._test_overlay
        )
        self.btn_overlay.grid(row=1, column=0, padx=4, pady=4, sticky="ew")

        self.btn_stop = ctk.CTkButton(
            btn_grid,
            text="Stop (Alt+Q)",
            fg_color="#f43f5e",
            hover_color="#e11d48",
            height=38,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._stop_loop
        )
        self.btn_stop.grid(row=1, column=1, padx=4, pady=4, sticky="ew")

        # Answer Result Card
        self.answer_card = AnswerCard(self.tab_hud)
        self.answer_card.pack(fill="both", expand=True, padx=10, pady=(8, 10))

    def _build_settings_tab(self):
        container = ctk.CTkScrollableFrame(self.tab_settings, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=6, pady=6)

        # 9router Base URL
        ctk.CTkLabel(container, text="9router Base URL:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(4, 2))
        self.entry_url = ctk.CTkEntry(container, height=34, corner_radius=6)
        self.entry_url.insert(0, self.config.get("router_base_url", "http://localhost:20128/v1"))
        self.entry_url.pack(fill="x", pady=2)

        # 9router API Key
        ctk.CTkLabel(container, text="9router API Key:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(8, 2))
        self.entry_key = ctk.CTkEntry(container, height=34, corner_radius=6, show="•")
        self.entry_key.insert(0, self.config.get("router_api_key", ""))
        self.entry_key.pack(fill="x", pady=2)

        # Primary Vision Model
        ctk.CTkLabel(container, text="Primary Vision Model:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(8, 2))
        self.entry_model = ctk.CTkEntry(container, height=34, corner_radius=6)
        self.entry_model.insert(0, self.config.get("primary_vision_model", "ag/gemini-3.8-flash-high"))
        self.entry_model.pack(fill="x", pady=2)

        # Fallback Vision Model
        ctk.CTkLabel(container, text="Fallback Vision Model:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(8, 2))
        self.entry_fallback = ctk.CTkEntry(container, height=34, corner_radius=6)
        self.entry_fallback.insert(0, self.config.get("fallback_vision_model", "ag/gemini-3.8-flash-high"))
        self.entry_fallback.pack(fill="x", pady=2)

        # Browser CDP Port / URL
        ctk.CTkLabel(container, text="Browser CDP URL:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(8, 2))
        self.entry_cdp = ctk.CTkEntry(container, height=34, corner_radius=6)
        self.entry_cdp.insert(0, self.config.get("browser_cdp_url", "http://localhost:9222"))
        self.entry_cdp.pack(fill="x", pady=2)

        # Delay Slider
        current_delay = float(self.config.get("action_delay", 1.0))
        self.lbl_delay = ctk.CTkLabel(container, text=f"Action Delay: {current_delay:.1f}s", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_delay.pack(anchor="w", pady=(10, 2))

        self.slider_delay = ctk.CTkSlider(
            container,
            from_=0.2,
            to=4.0,
            number_of_steps=38,
            command=self._on_slider_change
        )
        self.slider_delay.set(current_delay)
        self.slider_delay.pack(fill="x", pady=2)

        # Switches
        self.switch_submit = ctk.CTkSwitch(
            container,
            text="Auto-Submit Final Question (Safety Guard: OFF by default)",
            font=ctk.CTkFont(size=11)
        )
        if self.config.get("auto_submit_final", False):
            self.switch_submit.select()
        self.switch_submit.pack(anchor="w", pady=(12, 4))

        self.switch_antiblur = ctk.CTkSwitch(
            container,
            text="Anti-Blur / Prevent Tab-Switch Detection",
            font=ctk.CTkFont(size=11)
        )
        if self.config.get("prevent_blur_detection", True):
            self.switch_antiblur.select()
        self.switch_antiblur.pack(anchor="w", pady=4)

        # Save Button
        self.btn_save = ctk.CTkButton(
            container,
            text="💾 Save Settings",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#059669",
            hover_color="#047857",
            height=36,
            corner_radius=8,
            command=self._save_settings
        )
        self.btn_save.pack(fill="x", pady=(18, 10))

    def _on_topmost_toggle(self):
        is_top = bool(self.cb_topmost.get())
        self.attributes("-topmost", is_top)
        self.config.set("always_on_top", is_top)

    def _apply_always_on_top(self):
        is_top = self.config.get("always_on_top", True)
        self.attributes("-topmost", is_top)

    def _on_slider_change(self, val):
        self.lbl_delay.configure(text=f"Action Delay: {val:.1f}s")

    def _on_mode_change(self, selected_label):
        val = "auto_click_answer_only"
        for label, mode_key in MODE_LABELS:
            if label == selected_label:
                val = mode_key
                break

        self.config.set("execution_mode", val)
        self.lbl_mode_desc.configure(text=MODE_DESCRIPTIONS.get(val, ""))

    def _launch_chrome(self):
        success = self.worker.browser_engine.launch_debug_browser(9222)
        if success:
            self._on_worker_status("Browser Launched", "Chrome port 9222 terbuka. Menghubungkan...")
            self.worker.dispatch("connect_browser")
        else:
            self._on_worker_status("Error", "Chrome/Edge tidak ditemukan otomatis.")

    def _solve_once(self):
        self.worker.dispatch("solve_once")

    def _start_loop(self):
        self.worker.dispatch("auto_loop")

    def _test_overlay(self):
        self.worker.dispatch("test_overlay")

    def _stop_loop(self):
        self.worker.stop_loop()

    def _save_settings(self):
        url = self.entry_url.get().strip()
        if not validate_url(url):
            self._on_worker_status("Error", "URL endpoint tidak valid (wajib http:// atau https://)")
            return

        new_data = {
            "router_base_url": url,
            "router_api_key": self.entry_key.get().strip(),
            "primary_vision_model": self.entry_model.get().strip(),
            "fallback_vision_model": self.entry_fallback.get().strip(),
            "browser_cdp_url": self.entry_cdp.get().strip(),
            "action_delay": round(self.slider_delay.get(), 2),
            "auto_submit_final": bool(self.switch_submit.get()),
            "prevent_blur_detection": bool(self.switch_antiblur.get())
        }
        try:
            self.config.save(new_data)
            self.worker.llm_client.reload_config()
            self._on_worker_status("Saved", "Pengaturan berhasil disimpan.")
        except Exception as e:
            self._on_worker_status("Error", f"Gagal simpan: {e}")

    def _setup_hotkeys(self):
        if not keyboard:
            logger.info("Modul keyboard tidak aktif di lingkungan saat ini.")
            return
        try:
            keyboard.add_hotkey("alt+s", lambda: self.after(0, self._solve_once))
            keyboard.add_hotkey("alt+a", lambda: self.after(0, self._start_loop))
            keyboard.add_hotkey("alt+q", lambda: self.after(0, self._stop_loop))
        except Exception as e:
            logger.warning(f"Global hotkeys tidak dapat dipasang: {e}")

    def _on_worker_status(self, status: str, message: str):
        self.after(0, lambda: self._update_status(status, message))

    def _update_status(self, status: str, message: str):
        self.status_badge.set_status(status)
        self.lbl_status_msg.configure(text=message)

    def _on_worker_result(self, analysis: Dict[str, Any]):
        self.after(0, lambda: self._update_result(analysis))

    def _update_result(self, analysis: Dict[str, Any]):
        q_type = analysis.get("question_type", "unknown")
        correct_ids = analysis.get("correct_option_ids", [])
        reasoning = analysis.get("reasoning", "")
        self.answer_card.update_data(q_type, correct_ids, reasoning)

    def _on_close(self):
        self.worker.stop_loop()
        self.worker.dispatch("exit")
        self.destroy()
