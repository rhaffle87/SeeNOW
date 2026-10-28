# gui/components.py
import customtkinter as ctk

class StatusBadge(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#111827", corner_radius=14, border_width=1, border_color="#1f2937", **kwargs)
        self.dot = ctk.CTkLabel(
            self,
            text="●",
            font=ctk.CTkFont(size=10),
            text_color="#94a3b8",
            width=12
        )
        self.dot.pack(side="left", padx=(8, 2), pady=3)

        self.label = ctk.CTkLabel(
            self,
            text="IDLE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#94a3b8"
        )
        self.label.pack(side="left", padx=(0, 10), pady=3)

    def set_status(self, status: str):
        self.label.configure(text=status.upper())
        st = status.lower()
        if "idle" in st or "connected" in st or "saved" in st:
            self.configure(border_color="#065f46", fg_color="#064e3b")
            self.dot.configure(text_color="#34d399")
            self.label.configure(text_color="#a7f3d0")
        elif "capturing" in st or "thinking" in st or "testing" in st:
            self.configure(border_color="#92400e", fg_color="#78350f")
            self.dot.configure(text_color="#fbbf24")
            self.label.configure(text_color="#fde68a")
        elif "clicking" in st or "navigating" in st or "auto-loop" in st:
            self.configure(border_color="#1e40af", fg_color="#1e3a8a")
            self.dot.configure(text_color="#60a5fa")
            self.label.configure(text_color="#bfdbfe")
        elif "error" in st:
            self.configure(border_color="#991b1b", fg_color="#7f1d1d")
            self.dot.configure(text_color="#f87171")
            self.label.configure(text_color="#fecaca")
        else:
            self.configure(border_color="#1f2937", fg_color="#111827")
            self.dot.configure(text_color="#94a3b8")
            self.label.configure(text_color="#cbd5e1")

class MetricPill(ctk.CTkFrame):
    def __init__(self, master, label: str, value: str = "-", val_color: str = "#38bdf8", **kwargs):
        super().__init__(master, fg_color="#1e293b", corner_radius=8, border_width=1, border_color="#334155", **kwargs)
        self.lbl_title = ctk.CTkLabel(self, text=label, font=ctk.CTkFont(size=10, weight="bold"), text_color="#94a3b8")
        self.lbl_title.pack(anchor="w", padx=10, pady=(6, 0))

        self.lbl_val = ctk.CTkLabel(self, text=value, font=ctk.CTkFont(size=12, weight="bold"), text_color=val_color)
        self.lbl_val.pack(anchor="w", padx=10, pady=(0, 6))

    def set_value(self, value: str):
        self.lbl_val.configure(text=value)

class AnswerCard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#0f172a", corner_radius=10, border_width=1, border_color="#1e293b", **kwargs)

        # Header metric pill container (2 kolom)
        self.metric_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.metric_frame.pack(fill="x", padx=10, pady=(10, 6))
        self.metric_frame.grid_columnconfigure((0, 1), weight=1)

        self.pill_type = MetricPill(self.metric_frame, label="QUESTION TYPE", value="-", val_color="#38bdf8")
        self.pill_type.grid(row=0, column=0, padx=(0, 4), sticky="ew")

        self.pill_target = MetricPill(self.metric_frame, label="TARGET OPTION", value="-", val_color="#4ade80")
        self.pill_target.grid(row=0, column=1, padx=(4, 0), sticky="ew")

        # Label reasoning
        self.lbl_reasoning_title = ctk.CTkLabel(
            self,
            text="ANALYTICAL PROOF & REASONING",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#64748b"
        )
        self.lbl_reasoning_title.pack(anchor="w", padx=12, pady=(6, 2))

        # Textbox reasoning monospace
        self.txt_reasoning = ctk.CTkTextbox(
            self,
            height=130,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#020617",
            text_color="#e2e8f0",
            border_width=1,
            border_color="#1e293b",
            corner_radius=6,
            wrap="word"
        )
        self.txt_reasoning.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def update_data(self, q_type: str, selected_ids: list, reasoning: str):
        display_type = q_type.upper() if q_type else "UNKNOWN"
        self.pill_type.set_value(display_type)

        if selected_ids:
            display_opts = f"ID {selected_ids}"
        else:
            display_opts = "None / Read-Only"
        self.pill_target.set_value(display_opts)

        self.txt_reasoning.delete("1.0", "end")
        self.txt_reasoning.insert("1.0", reasoning or "Belum ada analisis.")
