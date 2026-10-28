# main.py
import logging
from core.logger_setup import setup_logging
from core.config_manager import ConfigManager
from gui.app_window import VisionQuizApp

# Setup structured rotating JSON logging
setup_logging()

logger = logging.getLogger("SeeNOW.Main")

def main():
    logger.info("Memulai SeeNOW (Smart Exam Engine & Navigated Optical Workflow)...")
    config = ConfigManager()
    app = VisionQuizApp(config)
    app.mainloop()

if __name__ == "__main__":
    main()
