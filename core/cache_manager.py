# core/cache_manager.py
import os
import re
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

        def is_option_candidate(el: Dict[str, Any]) -> bool:
            t = normalize_text(el.get("text", ""))
            # Abaikan navigasi
            if any(w in t for w in ("next", "submit", "finish", "selanjutnya", "kirim", "start", "prev", "back")):
                return False
            tag = (el.get("tag") or "").lower()
            role = (el.get("role") or "").lower()
            return tag in ("input", "label") or role in ("radio", "checkbox", "option") or len(t) > 0

        option_elements = [el for el in current_elements if is_option_candidate(el)]

        for cached_t in cached_correct_texts:
            best_match_id = None
            for el in option_elements:
                el_text = normalize_text(el.get("text", ""))
                if not el_text:
                    continue

                # 1. Exact match
                if el_text == cached_t:
                    best_match_id = el["id"]
                    break

                # 2. Match awalan (strip A. B. C. D.)
                clean_el_text = re.sub(r'^[a-z]\s*[\.\:\-\)]\s*', '', el_text).strip()
                clean_cached = re.sub(r'^[a-z]\s*[\.\:\-\)]\s*', '', cached_t).strip()
                if clean_el_text and clean_cached and (clean_el_text == clean_cached):
                    best_match_id = el["id"]
                    break

                # 3. Substring match hanya untuk teks panjang (minimal 5 karakter)
                if len(cached_t) >= 5 and len(el_text) >= 5:
                    if cached_t in el_text or el_text in cached_t:
                        best_match_id = el["id"]
                        break

            if best_match_id is not None and best_match_id not in matched_option_ids:
                matched_option_ids.append(best_match_id)

        # Cari tombol navigasi Next (eksplisit forward button)
        next_button_id: Optional[int] = None
        forward_keywords = ("next", "selanjutnya", "berikut", "lanjut", "finish", "submit", "kirim", "selesai")
        backward_keywords = ("prev", "previous", "kembali", "sebelumnya", "back", "prv")

        for el in current_elements:
            el_text = normalize_text(el.get("text", ""))
            if any(bw in el_text for bw in backward_keywords):
                continue
            if any(kw in el_text for kw in forward_keywords):
                next_button_id = el["id"]
                break

        return matched_option_ids, next_button_id
