# gui/components.py
import customtkinter as ctk

class StatusBadge(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#18181b", corner_radius=12, border_width=1, border_color="#27272a", **kwargs)
        self.dot = ctk.CTkLabel(
            self,
            text="●",
            font=ctk.CTkFont(size=9),
            text_color="#71717a",
            width=10
        )
        self.dot.pack(side="left", padx=(6, 2), pady=2)

        self.label = ctk.CTkLabel(
            self,
            text="IDLE",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#a1a1aa"
        )
        self.label.pack(side="left", padx=(0, 6), pady=2)

    def set_status(self, status: str):
        upper_text = status.upper()[:16]
        st = status.lower()
        if "idle" in st or "saved" in st:
            self.configure(border_color="#27272a", fg_color="#18181b")
            self.dot.configure(text_color="#71717a")
            self.label.configure(text=upper_text, text_color="#a1a1aa")
        elif "connected" in st or "exam loaded" in st:
            self.configure(border_color="#065f46", fg_color="#064e3b")
            self.dot.configure(text_color="#34d399")
            self.label.configure(text=upper_text, text_color="#a7f3d0")
        elif "capturing" in st or "thinking" in st or "starting" in st or "waiting" in st:
            self.configure(border_color="#78350f", fg_color="#451a03")
            self.dot.configure(text_color="#fbbf24")
            self.label.configure(text=upper_text, text_color="#fef08a")
        elif "clicking" in st or "navigating" in st or "auto-loop" in st or "loop" in st:
            self.configure(border_color="#1e3a8a", fg_color="#172554")
            self.dot.configure(text_color="#60a5fa")
            self.label.configure(text=upper_text, text_color="#bfdbfe")
        elif "error" in st:
            self.configure(border_color="#881337", fg_color="#4c0519")
            self.dot.configure(text_color="#f43f5e")
            self.label.configure(text=upper_text, text_color="#fecdd3")
        else:
            self.configure(border_color="#27272a", fg_color="#18181b")
            self.dot.configure(text_color="#a1a1aa")
            self.label.configure(text=upper_text, text_color="#e4e4e7")

class AnswerCard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#121215", corner_radius=8, border_width=1, border_color="#27272a", **kwargs)

        # Top Result Strip
        self.strip_frame = ctk.CTkFrame(self, fg_color="#18181b", height=28, corner_radius=6)
        self.strip_frame.pack(fill="x", padx=6, pady=(6, 4))

        self.lbl_type = ctk.CTkLabel(
            self.strip_frame,
            text="TYPE: —",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#a1a1aa"
        )
        self.lbl_type.pack(side="left", padx=8, pady=3)

        self.lbl_target = ctk.CTkLabel(
            self.strip_frame,
            text="TARGET: —",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#34d399"
        )
        self.lbl_target.pack(side="right", padx=8, pady=3)

        # Reasoning Textbox fills remaining space
        self.txt_reasoning = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#09090b",
            text_color="#e4e4e7",
            border_width=1,
            border_color="#27272a",
            corner_radius=6,
            wrap="word"
        )
        self.txt_reasoning.pack(fill="both", expand=True, padx=6, pady=(0, 6))

    def update_data(self, q_type: str, selected_ids: list, reasoning: str):
        display_type = f"TYPE: {q_type.upper()}" if q_type else "TYPE: —"
        self.lbl_type.configure(text=display_type)

        if selected_ids:
            display_opts = f"✔ OPTION ID: {selected_ids}"
            self.lbl_target.configure(text=display_opts, text_color="#34d399")
        else:
            self.lbl_target.configure(text="TARGET: READ-ONLY / NONE", text_color="#a1a1aa")

        self.txt_reasoning.delete("1.0", "end")
        self.txt_reasoning.insert("1.0", reasoning or "Belum ada analisis.")
