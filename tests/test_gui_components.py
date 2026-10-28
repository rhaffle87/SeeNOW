# tests/test_gui_components.py
from unittest.mock import MagicMock, patch

def test_status_badge_logic():
    with patch("customtkinter.CTkFrame.__init__", return_value=None), \
         patch("customtkinter.CTkLabel", return_value=MagicMock()), \
         patch("customtkinter.CTkFont", return_value=MagicMock()):
        from gui.components import StatusBadge
        badge = StatusBadge(MagicMock())
        badge.dot = MagicMock()
        badge.label = MagicMock()
        badge.configure = MagicMock()

        badge.set_status("idle")
        badge.label.configure.assert_called_with(text="IDLE", text_color="#a1a1aa")

        badge.set_status("thinking")
        badge.label.configure.assert_called_with(text="THINKING", text_color="#fef08a")

def test_answer_card_update():
    with patch("customtkinter.CTkFrame.__init__", return_value=None), \
         patch("customtkinter.CTkFrame.pack", return_value=None), \
         patch("customtkinter.CTkLabel", return_value=MagicMock()), \
         patch("customtkinter.CTkTextbox", return_value=MagicMock()), \
         patch("customtkinter.CTkFont", return_value=MagicMock()):
        from gui.components import AnswerCard
        card = AnswerCard(MagicMock())
        card.lbl_type = MagicMock()
        card.lbl_target = MagicMock()
        card.txt_reasoning = MagicMock()

        card.update_data("single_choice", [2], "Test reasoning")
        card.lbl_type.configure.assert_called_with(text="TYPE: SINGLE_CHOICE")
        card.lbl_target.configure.assert_called_with(text="✔ OPTION ID: [2]", text_color="#34d399")
        card.txt_reasoning.delete.assert_called_with("1.0", "end")
        card.txt_reasoning.insert.assert_called_with("1.0", "Test reasoning")
