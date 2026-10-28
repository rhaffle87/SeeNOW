# main.py
import sys
import logging
from core.config_manager import ConfigManager
from gui.app_window import VisionQuizApp

# Setup structured logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", "message": "%(message)s"}',
    stream=sys.stdout
)

# Mute noisy internal loggers agar log terminal bersih, terfokus, dan bebas polusi HTTP spam
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("openai._base_client").setLevel(logging.WARNING)

logger = logging.getLogger("SeeNOW.Main")

def main():
    logger.info("Memulai SeeNOW (Smart Exam Engine & Navigated Optical Workflow)...")
    config = ConfigManager()
    app = VisionQuizApp(config)
    app.mainloop()

if __name__ == "__main__":
    main()
