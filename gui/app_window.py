# gui/app_window.py
import os
import sys
import logging
import customtkinter as ctk
from typing import Dict, Any, List
from core.config_manager import ConfigManager, validate_url, get_base_dir
from core.agent_worker import AgentWorker
from gui.components import StatusBadge, AnswerCard, add_tooltip

logger = logging.getLogger("SeeNOW.GUI")

try:
    import keyboard
except Exception:
    keyboard = None  # type: ignore

MODE_MAP_TO_KEY = {
    "🎯 Click": "auto_click_answer_only",
    "⚡ Auto": "auto_click_and_next",
    "👁️ Read": "read_only"
}

MODE_MAP_TO_DISPLAY = {
    "auto_click_answer_only": "🎯 Click",
    "auto_click_and_next": "⚡ Auto",
    "read_only": "👁️ Read"
}

class VisionQuizApp(ctk.CTk):
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config = config_manager
        self.open_tabs_list: List[Dict[str, Any]] = []

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("SeeNOW HUD")
        self.geometry("380x430")
        self.minsize(310, 125)
        self.resizable(True, True)
        self.configure(fg_color="#09090b")

        # State flags
        self.is_compact = False
        self.is_settings_open = False
        self.prev_geometry = "380x430"
        self.alpha_levels = [1.0, 0.82, 0.60]
        self.alpha_idx = 0

        # Background worker
        self.worker = AgentWorker(
            config_manager=self.config,
            status_callback=self._on_worker_status,
            result_callback=self._on_worker_result,
            tabs_callback=self._on_tabs_updated
        )
        self.worker.start()

        self._build_ui()
        self._setup_hotkeys()
        self._apply_always_on_top()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        # Configure root grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Row 0: Header
        self.grid_rowconfigure(1, weight=0)  # Row 1: Connection & Mode
        self.grid_rowconfigure(2, weight=0)  # Row 2: Command Toolbar
        self.grid_rowconfigure(3, weight=1)  # Row 3: Workspace (expands!)
        self.grid_rowconfigure(4, weight=0)  # Row 4: Status footer

        # ==========================================
        # ROW 0: Ultra-Slim Header Bar (height=32)
        # ==========================================
        self.header_frame = ctk.CTkFrame(self, fg_color="#121215", corner_radius=0, height=32, border_width=1, border_color="#27272a")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        # Header Left
        hdr_left = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        hdr_left.pack(side="left", padx=(8, 4), pady=3)

        lbl_logo = ctk.CTkLabel(hdr_left, text="SeeNOW", font=ctk.CTkFont(size=12, weight="bold"), text_color="#f4f4f5")
        lbl_logo.pack(side="left", padx=(0, 6))

        self.status_badge = StatusBadge(hdr_left)
        self.status_badge.pack(side="left", padx=(0, 6))

        self.lbl_quick_ans = ctk.CTkLabel(
            hdr_left,
            text="ANS: —",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#34d399"
        )
        self.lbl_quick_ans.pack(side="left", padx=(2, 0))

        # Header Right (Icon Tools)
        hdr_right = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        hdr_right.pack(side="right", padx=(4, 6), pady=3)

        self.btn_opacity = ctk.CTkButton(
            hdr_right,
            text="◐",
            width=24,
            height=22,
            font=ctk.CTkFont(size=11),
            fg_color="#18181b",
            hover_color="#27272a",
            text_color="#a1a1aa",
            corner_radius=4,
            command=self._cycle_opacity
        )
        self.btn_opacity.pack(side="left", padx=2)

        self.btn_pin = ctk.CTkButton(
            hdr_right,
            text="📌",
            width=24,
            height=22,
            font=ctk.CTkFont(size=10),
            fg_color="#18181b",
            hover_color="#27272a",
            text_color="#38bdf8" if self.config.get("always_on_top", True) else "#71717a",
            corner_radius=4,
            command=self._toggle_pin
        )
        self.btn_pin.pack(side="left", padx=2)

        self.btn_compact = ctk.CTkButton(
            hdr_right,
            text="🔽",
            width=24,
            height=22,
            font=ctk.CTkFont(size=10),
            fg_color="#18181b",
            hover_color="#27272a",
            text_color="#a1a1aa",
            corner_radius=4,
            command=self._toggle_compact
        )
        self.btn_compact.pack(side="left", padx=2)

        self.btn_settings = ctk.CTkButton(
            hdr_right,
            text="⚙️",
            width=24,
            height=22,
            font=ctk.CTkFont(size=11),
            fg_color="#18181b",
            hover_color="#27272a",
            text_color="#a1a1aa",
            corner_radius=4,
            command=self._toggle_settings
        )
        self.btn_settings.pack(side="left", padx=2)

        # ==========================================
        # ROW 1: Connection & Mode Bar (height=30)
        # ==========================================
        self.row_conn = ctk.CTkFrame(self, fg_color="#121215", height=30, corner_radius=6, border_width=1, border_color="#27272a")
        self.row_conn.grid(row=1, column=0, sticky="ew", padx=6, pady=(4, 2))

        # Attach Browser
        self.btn_attach = ctk.CTkButton(
            self.row_conn,
            text="🌐 Attach",
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color="#18181b",
            hover_color="#27272a",
            text_color="#e4e4e7",
            height=24,
            width=68,
            corner_radius=4,
            command=self._launch_chrome
        )
        self.btn_attach.pack(side="left", padx=(6, 4), pady=3)

        # Target Tab Menu
        self.tab_menu_var = ctk.StringVar(value="[No Tabs]")
        self.tab_menu = ctk.CTkOptionMenu(
            self.row_conn,
            variable=self.tab_menu_var,
            values=["[No Tabs]"],
            font=ctk.CTkFont(size=10),
            fg_color="#18181b",
            button_color="#27272a",
            button_hover_color="#3f3f46",
            height=24,
            width=120,
            corner_radius=4,
            command=self._on_tab_selected
        )
        self.tab_menu.pack(side="left", fill="x", expand=True, padx=(0, 2), pady=3)

        self.btn_refresh = ctk.CTkButton(
            self.row_conn,
            text="🔄",
            width=24,
            height=24,
            font=ctk.CTkFont(size=10),
            fg_color="#18181b",
            hover_color="#27272a",
            text_color="#a1a1aa",
            corner_radius=4,
            command=self._refresh_tabs
        )
        self.btn_refresh.pack(side="left", padx=(2, 6), pady=3)

        # Mode Selector Menu
        current_mode_key = self.config.get("execution_mode", "auto_click_answer_only")
        init_mode_display = MODE_MAP_TO_DISPLAY.get(current_mode_key, "🎯 Click")
        self.mode_menu_var = ctk.StringVar(value=init_mode_display)
        self.mode_menu = ctk.CTkOptionMenu(
            self.row_conn,
            variable=self.mode_menu_var,
            values=["🎯 Click", "⚡ Auto", "👁️ Read"],
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color="#18181b",
            button_color="#27272a",
            button_hover_color="#3f3f46",
            height=24,
            width=90,
            corner_radius=4,
            command=self._on_mode_selected
        )
        self.mode_menu.pack(side="right", padx=(0, 6), pady=3)

        # ==========================================
        # ROW 2: Unified Command Toolbar (height=32)
        # ==========================================
        self.row_tools = ctk.CTkFrame(self, fg_color="transparent")
        self.row_tools.grid(row=2, column=0, sticky="ew", padx=6, pady=(2, 4))

        self.btn_solve = ctk.CTkButton(
            self.row_tools,
            text="▶ Solve",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            text_color="#ffffff",
            height=28,
            corner_radius=6,
            command=self._solve_once
        )
        self.btn_solve.pack(side="left", fill="x", expand=True, padx=(0, 3))

        self.btn_loop = ctk.CTkButton(
            self.row_tools,
            text="⚡ Auto",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            text_color="#ffffff",
            height=28,
            corner_radius=6,
            command=self._start_loop
        )
        self.btn_loop.pack(side="left", fill="x", expand=True, padx=3)

        self.btn_stop = ctk.CTkButton(
            self.row_tools,
            text="⏹ Stop",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#18181b",
            hover_color="#27272a",
            text_color="#a1a1aa",
            border_width=1,
            border_color="#27272a",
            width=54,
            height=28,
            corner_radius=6,
            command=self._stop_loop
        )
        self.btn_stop.pack(side="left", padx=3)

        self.btn_overlay = ctk.CTkButton(
            self.row_tools,
            text="🎯",
            width=28,
            height=28,
            font=ctk.CTkFont(size=11),
            fg_color="#18181b",
            hover_color="#27272a",
            text_color="#e4e4e7",
            border_width=1,
            border_color="#27272a",
            corner_radius=6,
            command=self._test_overlay
        )
        self.btn_overlay.pack(side="left", padx=2)

        self.btn_export = ctk.CTkButton(
            self.row_tools,
            text="📄",
            width=28,
            height=28,
            font=ctk.CTkFont(size=11),
            fg_color="#18181b",
            hover_color="#27272a",
            text_color="#e4e4e7",
            border_width=1,
            border_color="#27272a",
            corner_radius=6,
            command=self._export_notary
        )
        self.btn_export.pack(side="left", padx=(2, 0))

        # ==========================================
        # ROW 3: Workspace Area (AnswerCard & Settings)
        # ==========================================
        self.workspace_container = ctk.CTkFrame(self, fg_color="transparent")
        self.workspace_container.grid(row=3, column=0, sticky="nsew", padx=6, pady=(0, 2))
        self.workspace_container.grid_rowconfigure(0, weight=1)
        self.workspace_container.grid_columnconfigure(0, weight=1)

        # Main Answer Card
        self.answer_card = AnswerCard(self.workspace_container)
        self.answer_card.grid(row=0, column=0, sticky="nsew")

        # Inline Settings Drawer (initially hidden)
        self._build_settings_drawer()

        # ==========================================
        # ROW 4: Ultra-Slim Status Bar (height=18)
        # ==========================================
        self.status_bar = ctk.CTkFrame(self, fg_color="#09090b", height=18, corner_radius=0)
        self.status_bar.grid(row=4, column=0, sticky="ew", padx=8, pady=(0, 2))

        self.lbl_status_msg = ctk.CTkLabel(
            self.status_bar,
            text="Siap dijalankan (Alt+S untuk uji 1 soal).",
            font=ctk.CTkFont(size=10),
            text_color="#71717a",
            anchor="w"
        )
        self.lbl_status_msg.pack(side="left", fill="x", expand=True)

        self._attach_tooltips()

    def _attach_tooltips(self):
        add_tooltip(self.btn_attach, "Launches local Chrome/Edge on CDP port 9222 with persistent profile, or attaches if already running.")
        add_tooltip(self.tab_menu, "Selects the active quiz iframe/tab or refreshes the list of open browser tabs.")
        add_tooltip(self.btn_refresh, "Refreshes the list of open browser tabs.")
        add_tooltip(self.mode_menu, "Click: Solves & selects answer manually | Auto: Solves, clicks answer & auto-advances Next | Read-Only: Displays proof without clicking browser DOM.")
        add_tooltip(self.btn_solve, "Captures current screen, queries 9router LLM, records notary log, and executes selected answer(s) (Alt+S).")
        add_tooltip(self.btn_loop, "Continuously runs the Observe-Think-Act loop across all quiz questions until the final submit page (Alt+A).")
        add_tooltip(self.btn_stop, "Immediately halts the continuous auto-loop process (Alt+Q).")
        add_tooltip(self.btn_overlay, "Injects red Set-of-Marks [ID] bounding boxes on live browser for 3 seconds to verify visual element detection.")
        add_tooltip(self.btn_export, "Exports all recorded session questions, reasoning proofs, and correct answers into a formatted Markdown report (.md).")
        add_tooltip(self.btn_compact, "Collapses the window into a sleek Mini-Bar (360x125) or expands to full HUD workspace.")
        add_tooltip(self.btn_opacity, "Cycles window transparency (100% -> 82% -> 60%) so underlying quiz questions remain visible.")
        add_tooltip(self.btn_pin, "Pins HUD window always-on-top above browser and other apps.")
        add_tooltip(self.btn_settings, "Toggles settings drawer for 9router API key, models, delay, and stealth options.")
        add_tooltip(self.status_badge, "Current execution status of the SeeNOW agent.")

    def _build_settings_drawer(self):
        self.settings_frame = ctk.CTkScrollableFrame(
            self.workspace_container,
            fg_color="#121215",
            corner_radius=8,
            border_width=1,
            border_color="#27272a"
        )
        # Hidden by default

        # 9router Base URL
        ctk.CTkLabel(self.settings_frame, text="9router Base URL:", font=ctk.CTkFont(size=10, weight="bold"), text_color="#a1a1aa").pack(anchor="w", pady=(2, 1))
        self.entry_url = ctk.CTkEntry(self.settings_frame, height=28, corner_radius=4, font=ctk.CTkFont(size=11), fg_color="#18181b", border_color="#27272a")
        self.entry_url.insert(0, self.config.get("router_base_url", "http://localhost:20128/v1"))
        self.entry_url.pack(fill="x", pady=(0, 4))

        # 9router API Key
        ctk.CTkLabel(self.settings_frame, text="9router API Key:", font=ctk.CTkFont(size=10, weight="bold"), text_color="#a1a1aa").pack(anchor="w", pady=(2, 1))
        self.entry_key = ctk.CTkEntry(self.settings_frame, height=28, corner_radius=4, font=ctk.CTkFont(size=11), show="•", fg_color="#18181b", border_color="#27272a")
        self.entry_key.insert(0, self.config.get("router_api_key", ""))
        self.entry_key.pack(fill="x", pady=(0, 4))

        # Primary Vision Model
        ctk.CTkLabel(self.settings_frame, text="Primary Vision Model:", font=ctk.CTkFont(size=10, weight="bold"), text_color="#a1a1aa").pack(anchor="w", pady=(2, 1))
        self.entry_model = ctk.CTkEntry(self.settings_frame, height=28, corner_radius=4, font=ctk.CTkFont(size=11), fg_color="#18181b", border_color="#27272a")
        self.entry_model.insert(0, self.config.get("primary_vision_model", "ag/gemini-3.8-flash-high"))
        self.entry_model.pack(fill="x", pady=(0, 4))

        # Fallback Vision Model
        ctk.CTkLabel(self.settings_frame, text="Fallback Vision Model:", font=ctk.CTkFont(size=10, weight="bold"), text_color="#a1a1aa").pack(anchor="w", pady=(2, 1))
        self.entry_fallback = ctk.CTkEntry(self.settings_frame, height=28, corner_radius=4, font=ctk.CTkFont(size=11), fg_color="#18181b", border_color="#27272a")
        self.entry_fallback.insert(0, self.config.get("fallback_vision_model", "ag/gemini-3.8-flash-low"))
        self.entry_fallback.pack(fill="x", pady=(0, 4))

        # Browser CDP Port / URL
        ctk.CTkLabel(self.settings_frame, text="Browser CDP URL:", font=ctk.CTkFont(size=10, weight="bold"), text_color="#a1a1aa").pack(anchor="w", pady=(2, 1))
        self.entry_cdp = ctk.CTkEntry(self.settings_frame, height=28, corner_radius=4, font=ctk.CTkFont(size=11), fg_color="#18181b", border_color="#27272a")
        self.entry_cdp.insert(0, self.config.get("browser_cdp_url", "http://localhost:9222"))
        self.entry_cdp.pack(fill="x", pady=(0, 4))

        # Delay Slider
        current_delay = float(self.config.get("action_delay", 0.5))
        self.lbl_delay = ctk.CTkLabel(self.settings_frame, text=f"Action Delay: {current_delay:.1f}s", font=ctk.CTkFont(size=10, weight="bold"), text_color="#a1a1aa")
        self.lbl_delay.pack(anchor="w", pady=(4, 1))

        self.slider_delay = ctk.CTkSlider(
            self.settings_frame,
            from_=0.1,
            to=3.0,
            number_of_steps=29,
            height=14,
            command=self._on_slider_change
        )
        self.slider_delay.set(current_delay)
        self.slider_delay.pack(fill="x", pady=(0, 6))

        # Switches
        self.switch_submit = ctk.CTkSwitch(
            self.settings_frame,
            text="Auto-Submit Final Question",
            font=ctk.CTkFont(size=10),
            height=20
        )
        if self.config.get("auto_submit_final", False):
            self.switch_submit.select()
        self.switch_submit.pack(anchor="w", pady=2)

        self.switch_antiblur = ctk.CTkSwitch(
            self.settings_frame,
            text="Anti-Blur / Prevent Proctoring Tab-Switch",
            font=ctk.CTkFont(size=10),
            height=20
        )
        if self.config.get("prevent_blur_detection", True):
            self.switch_antiblur.select()
        self.switch_antiblur.pack(anchor="w", pady=2)

        self.switch_cache = ctk.CTkSwitch(
            self.settings_frame,
            text="Smart Cache (Zero-latency repeat solve)",
            font=ctk.CTkFont(size=10),
            height=20
        )
        if self.config.get("enable_question_cache", True):
            self.switch_cache.select()
        self.switch_cache.pack(anchor="w", pady=2)

        # Settings Buttons
        btn_box = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        btn_box.pack(fill="x", pady=(8, 4))

        self.btn_save = ctk.CTkButton(
            btn_box,
            text="💾 Save",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#059669",
            hover_color="#047857",
            height=28,
            corner_radius=4,
            command=self._save_settings
        )
        self.btn_save.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.btn_view_logs = ctk.CTkButton(
            btn_box,
            text="📄 Logs",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#18181b",
            hover_color="#27272a",
            height=28,
            width=60,
            corner_radius=4,
            command=self._export_log
        )
        self.btn_view_logs.pack(side="right")

    def _toggle_settings(self):
        if self.is_compact:
            self._toggle_compact()

        if self.is_settings_open:
            self.settings_frame.grid_forget()
            self.answer_card.grid(row=0, column=0, sticky="nsew")
            self.btn_settings.configure(fg_color="#18181b", text_color="#a1a1aa")
            self.is_settings_open = False
        else:
            self.answer_card.grid_forget()
            self.settings_frame.grid(row=0, column=0, sticky="nsew")
            self.btn_settings.configure(fg_color="#27272a", text_color="#38bdf8")
            self.is_settings_open = True

    def _cycle_opacity(self):
        self.alpha_idx = (self.alpha_idx + 1) % len(self.alpha_levels)
        val = self.alpha_levels[self.alpha_idx]
        self.attributes("-alpha", val)
        self._on_worker_status("Opacity", f"Tingkat transparansi jendela: {int(val * 100)}%")

    def _toggle_pin(self):
        current = self.config.get("always_on_top", True)
        new_val = not current
        self.config.set("always_on_top", new_val)
        self._apply_always_on_top()
        self.btn_pin.configure(text_color="#38bdf8" if new_val else "#71717a")
        self._on_worker_status("Pin", f"Always on Top: {'Aktif' if new_val else 'Nonaktif'}")

    def _toggle_compact(self):
        if not self.is_compact:
            # Switch to Mini-HUD mode (360x125)
            self.prev_geometry = self.geometry()
            self.is_compact = True
            self.btn_compact.configure(text="🔼")

            # Close settings if open
            if self.is_settings_open:
                self.settings_frame.grid_forget()
                self.btn_settings.configure(fg_color="#18181b", text_color="#a1a1aa")
                self.is_settings_open = False

            # Hide Row 1 (Connection) & Row 3 (Workspace)
            self.row_conn.grid_forget()
            self.workspace_container.grid_forget()

            self.geometry("360x125")
            self._on_worker_status("Compact", "Mini-HUD Mode aktif.")
        else:
            # Restore to full expanded mode
            self.is_compact = False
            self.btn_compact.configure(text="🔽")

            self.row_conn.grid(row=1, column=0, sticky="ew", padx=6, pady=(4, 2))
            self.workspace_container.grid(row=3, column=0, sticky="nsew", padx=6, pady=(0, 2))
            self.answer_card.grid(row=0, column=0, sticky="nsew")

            if self.prev_geometry:
                self.geometry(self.prev_geometry)
            else:
                self.geometry("380x430")
            self._on_worker_status("Expanded", "Expanded Mode aktif.")

    def _apply_always_on_top(self):
        val = self.config.get("always_on_top", True)
        self.attributes("-topmost", val)

    def _on_mode_selected(self, choice: str):
        key = MODE_MAP_TO_KEY.get(choice, "auto_click_answer_only")
        self.config.set("execution_mode", key)
        self._on_worker_status("Mode", f"Mode eksekusi: {choice}")

    def _launch_chrome(self):
        self._on_worker_status("Connecting", "Menghubungkan ke browser CDP...")
        self.worker.dispatch("connect_browser")

    def _solve_once(self):
        self.worker.dispatch("solve_once")

    def _start_loop(self):
        self.btn_stop.configure(fg_color="#3f1d24", border_color="#881337", text_color="#f43f5e")
        self.worker.dispatch("auto_loop")

    def _stop_loop(self):
        self.btn_stop.configure(fg_color="#18181b", border_color="#27272a", text_color="#a1a1aa")
        self.worker.stop_loop()

    def _test_overlay(self):
        self.worker.dispatch("test_overlay")

    def _on_slider_change(self, value):
        delay = round(value, 1)
        self.lbl_delay.configure(text=f"Action Delay: {delay}s")

    def _save_settings(self):
        url = self.entry_url.get().strip()
        if not validate_url(url):
            self._on_worker_status("Error", "URL 9router tidak valid. Harus diawali http:// atau https://")
            return

        new_data = {
            "router_base_url": url,
            "router_api_key": self.entry_key.get().strip(),
            "primary_vision_model": self.entry_model.get().strip(),
            "fallback_vision_model": self.entry_fallback.get().strip(),
            "browser_cdp_url": self.entry_cdp.get().strip(),
            "action_delay": round(self.slider_delay.get(), 2),
            "auto_submit_final": bool(self.switch_submit.get()),
            "prevent_blur_detection": bool(self.switch_antiblur.get()),
            "enable_question_cache": bool(self.switch_cache.get())
        }
        try:
            self.config.save(new_data)
            self.worker.llm_client.reload_config()
            self._on_worker_status("Saved", "Pengaturan berhasil disimpan.")
            self._toggle_settings()
        except Exception as e:
            self._on_worker_status("Error", f"Gagal simpan: {e}")

    def _export_log(self):
        log_path = os.path.join(get_base_dir(), "logs", "seenow.log")
        if os.path.isfile(log_path):
            if sys.platform == "win32":
                try:
                    os.startfile(log_path)  # type: ignore[attr-defined]
                    return
                except Exception:
                    pass
            self._on_worker_status("Log Path", f"Log tersimpan di: {log_path}")
        else:
            self._on_worker_status("Log Info", "Belum ada file log yang dibuat.")

    def _export_notary(self):
        try:
            md_path = self.worker.notary.export_markdown()
            count = len(self.worker.notary.records)
            self._on_worker_status("Notary Exported", f"Terekam {count} soal. Tersimpan: {os.path.basename(md_path)}")
            if sys.platform == "win32":
                try:
                    os.startfile(md_path)  # type: ignore[attr-defined]
                except Exception:
                    pass
        except Exception as e:
            self._on_worker_status("Error", f"Gagal ekspor notulensi: {e}")

    def _on_tabs_updated(self, tabs: List[Dict[str, Any]]):
        self.after(0, lambda: self._apply_tabs_update(tabs))

    def _apply_tabs_update(self, tabs: List[Dict[str, Any]]):
        self.open_tabs_list = tabs
        if not tabs:
            self.tab_menu.configure(values=["[No Tabs]"])
            self.tab_menu_var.set("[No Tabs]")
            return

        titles = []
        active_title = None
        for t in tabs:
            display = f"#{t['index']} {t['title'][:20]}"
            titles.append(display)
            if t.get("is_active"):
                active_title = display

        self.tab_menu.configure(values=titles)
        if active_title:
            self.tab_menu_var.set(active_title)
        elif titles:
            self.tab_menu_var.set(titles[0])

    def _on_tab_selected(self, choice: str):
        if not self.open_tabs_list or choice == "[No Tabs]":
            return
        try:
            idx_str = choice.split()[0].replace("#", "")
            idx = int(idx_str)
            self.worker.dispatch("select_tab", idx)
        except Exception:
            pass

    def _refresh_tabs(self):
        self.worker.dispatch("list_tabs")

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
        st = status.lower()
        if "connected" in st or "exam" in st:
            self.btn_attach.configure(text="🌐 Connected", text_color="#34d399")
        elif "idle" in st or "stopped" in st:
            self.btn_stop.configure(fg_color="#18181b", border_color="#27272a", text_color="#a1a1aa")
        elif "auto-loop" in st or "clicking" in st:
            self.btn_stop.configure(fg_color="#3f1d24", border_color="#881337", text_color="#f43f5e")

    def _on_worker_result(self, analysis: Dict[str, Any]):
        self.after(0, lambda: self._update_result(analysis))

    def _update_result(self, analysis: Dict[str, Any]):
        q_type = analysis.get("question_type", "unknown")
        correct_ids = analysis.get("correct_option_ids", [])
        reasoning = analysis.get("reasoning", "")
        self.answer_card.update_data(q_type, correct_ids, reasoning)
        if correct_ids:
            self.lbl_quick_ans.configure(text=f"ANS: {correct_ids}", text_color="#34d399")
        else:
            self.lbl_quick_ans.configure(text="ANS: —", text_color="#a1a1aa")

    def _on_close(self):
        self.worker.stop_loop()
        self.worker.dispatch("exit")
        self.destroy()
