# core/cache_manager.py
import os
import json
import hashlib
import logging
import threading
from typing import Dict, Any, Optional, List, Tuple
from core.config_manager import get_base_dir

logger = logging.getLogger("SeeNOW.Cache")

def normalize_text(text: str) -> str:
    return " ".join((text or "").strip().lower().split())

def compute_question_cache_key(page_text: str, option_texts: List[str]) -> str:
    norm_page = normalize_text(page_text)
    # Sort option texts to ensure order-invariant matching if options shuffle
    sorted_opts = sorted([normalize_text(opt) for opt in option_texts if opt.strip()])
    combined = f"{norm_page[:600]}|{'|'.join(sorted_opts)}"
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()

class QuestionCacheManager:
    def __init__(self, cache_file: Optional[str] = None, max_entries: int = 1000):
        if cache_file:
            self.cache_file = cache_file
        else:
            self.cache_file = os.path.join(get_base_dir(), "question_cache.json")
        self.max_entries = max_entries
        self.lock = threading.Lock()
        self.cache: Dict[str, Dict[str, Any]] = self._load()

    def _load(self) -> Dict[str, Dict[str, Any]]:
        if os.path.isfile(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
            except Exception as e:
                logger.warning(f"Gagal memuat question_cache.json: {e}")
        return {}

    def _persist(self):
        tmp_file = f"{self.cache_file}.tmp"
        try:
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_file, self.cache_file)
        except Exception as e:
            if os.path.exists(tmp_file):
                try:
                    os.remove(tmp_file)
                except Exception:
                    pass
            logger.warning(f"Gagal menyimpan question_cache.json: {e}")

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            entry = self.cache.get(key)
            if entry:
                # Refresh position for LRU
                del self.cache[key]
                self.cache[key] = entry
                return entry.copy()
            return None

    def put(self, key: str, data: Dict[str, Any]):
        with self.lock:
            if key in self.cache:
                del self.cache[key]
            elif len(self.cache) >= self.max_entries:
                # Evict oldest entry (first item)
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]

            self.cache[key] = data.copy()
            self._persist()

    def clear(self):
        with self.lock:
            self.cache.clear()
            if os.path.isfile(self.cache_file):
                try:
                    os.remove(self.cache_file)
                except Exception:
                    pass

    @staticmethod
    def resolve_cached_options(
        cached_entry: Dict[str, Any],
        current_elements: List[Dict[str, Any]]
    ) -> Tuple[List[int], Optional[int]]:
        """
        Remap teks jawaban yang tersimpan di cache ke nomor [ID] pada elemen layar saat ini,
        menangani kasus urutan opsi pilihan ganda yang diacak (shuffled).
        """
        cached_correct_texts = [normalize_text(t) for t in cached_entry.get("correct_option_texts", []) if t]
        matched_option_ids: List[int] = []

        for cached_t in cached_correct_texts:
            for el in current_elements:
                el_text = normalize_text(el.get("text", ""))
                # Cocokkan teks opsi
                if cached_t in el_text or el_text in cached_t:
                    if el["id"] not in matched_option_ids:
                        matched_option_ids.append(el["id"])
                        break

        # Cari tombol navigasi Next
        next_button_id: Optional[int] = None
        nav_keywords = ("next", "selanjutnya", "berikut", "lanjut", "finish", "selesai")
        for el in current_elements:
            el_text = normalize_text(el.get("text", ""))
            tag = el.get("tag", "").lower()
            role = el.get("role", "").lower()
            if any(kw in el_text for kw in nav_keywords) or ((tag == "button" or role == "button") and "next" in el_text):
                next_button_id = el["id"]
                break

        return matched_option_ids, next_button_id
