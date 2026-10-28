# core/os_screen_engine.py
import io
import base64
import logging
from typing import Tuple, Dict, Any, Optional
from PIL import Image

logger = logging.getLogger(__name__)

try:
    import mss
except Exception:
    mss = None  # type: ignore

try:
    import pyautogui
except Exception:
    pyautogui = None  # type: ignore

class OSScreenEngine:
    def __init__(self):
        self.sct: Optional[Any] = mss.mss() if mss else None
        if pyautogui:
            try:
                pyautogui.FAILSAFE = True
                pyautogui.PAUSE = 0.1
            except Exception:
                pass

    def capture_fullscreen(self) -> Tuple[str, Dict[str, Any]]:
        if not self.sct:
            raise RuntimeError("MSS screen capture library tidak tersedia di lingkungan saat ini.")

        # Tangkap monitor primer
        monitor = self.sct.monitors[1]
        sct_img = self.sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        metadata = {
            "width": monitor["width"],
            "height": monitor["height"],
            "left": monitor["left"],
            "top": monitor["top"]
        }
        return b64, metadata

    def click_coordinate(self, x: int, y: int, duration: float = 0.2):
        if not pyautogui:
            logger.warning("PyAutoGUI tidak tersedia di lingkungan saat ini.")
            return

        try:
            pyautogui.moveTo(x, y, duration=duration)
            pyautogui.click(x, y)
        except Exception as e:
            logger.error(f"Gagal melakukan klik OS-level pada ({x}, {y}): {e}")
