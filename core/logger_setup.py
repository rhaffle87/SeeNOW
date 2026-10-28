# core/logger_setup.py
import os
import sys
import json
import logging
import re
from logging.handlers import RotatingFileHandler
from core.config_manager import get_base_dir

SECRET_REGEX = re.compile(r"(sk-[a-zA-Z0-9_\-]{8,})|(key-[a-zA-Z0-9_\-]{8,})", re.IGNORECASE)

class MaskedJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        msg = record.getMessage()
        # Mask any token/secret in log message
        masked_msg = SECRET_REGEX.sub(r"\1"[:3] + "****" + r"\1"[-4:], msg) if SECRET_REGEX.search(msg) else msg

        log_obj = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "module": record.name,
            "message": masked_msg
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj, ensure_ascii=False)

def setup_logging() -> str:
    base_dir = get_base_dir()
    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "seenow.log")

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Clear existing handlers if any
    for h in list(root_logger.handlers):
        root_logger.removeHandler(h)

    formatter = MaskedJsonFormatter()

    # Stream Handler (stdout)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    root_logger.addHandler(stdout_handler)

    # Rotating File Handler (2 MB, 3 backups)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=2_000_000,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Mute noisy internal HTTP loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai._base_client").setLevel(logging.WARNING)

    return log_file
