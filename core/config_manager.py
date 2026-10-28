# core/config_manager.py
import os
import sys
import json
import logging
from typing import Dict, Any
from urllib.parse import urlparse

logger = logging.getLogger("SeeNOW.Config")

def get_base_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_CONFIG_PATH = os.path.join(get_base_dir(), "config.json")

DEFAULT_CONFIG: Dict[str, Any] = {
    "router_base_url": os.getenv("ROUTER_BASE_URL", "http://localhost:20128/v1"),
    "router_api_key": os.getenv("ROUTER_API_KEY", ""),
    "primary_vision_model": os.getenv("PRIMARY_VISION_MODEL", "ag/gemini-3.8-flash-high"),
    "fallback_vision_model": os.getenv("FALLBACK_VISION_MODEL", "ag/gemini-3.8-flash-high"),
    "browser_cdp_url": os.getenv("BROWSER_CDP_URL", "http://localhost:9222"),
    "execution_mode": "auto_click_answer_only",
    "action_delay": 1.0,
    "auto_submit_final": False,
    "always_on_top": True,
    "prevent_blur_detection": True,
    "request_timeout_sec": 25,
    "max_retries": 2
}

def mask_secret(secret: str) -> str:
    if not secret:
        return "[NOT SET]"
    if len(secret) <= 8:
        return "****"
    return secret[:3] + "****" + secret[-4:]

def validate_url(url: str) -> bool:
    if not url:
        return False
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)

class ConfigManager:
    def __init__(self, config_path: str = DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self.data: Dict[str, Any] = self.load()

    def load(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    cfg = DEFAULT_CONFIG.copy()
                    cfg.update(saved)
                    return cfg
            except Exception as e:
                logger.warning(f"Gagal membaca {self.config_path}: {e}")
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()

    def save(self, new_data: Dict[str, Any]):
        # Validasi URL sebelum menyimpan
        target_url = new_data.get("router_base_url", self.data.get("router_base_url", ""))
        if not validate_url(target_url):
            raise ValueError(f"URL endpoint tidak valid (wajib diawali http:// atau https://): {target_url}")

        self.data.update(new_data)
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            logger.info("Konfigurasi berhasil disimpan.")
        except Exception as e:
            logger.error(f"Gagal menulis file konfigurasi: {e}")
            raise e

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        self.data[key] = value
        self.save(self.data)
