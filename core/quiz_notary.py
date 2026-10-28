# core/quiz_notary.py
import json
import os
import time
import logging
from typing import Dict, Any, List, Optional
from core.config_manager import get_base_dir

logger = logging.getLogger("SeeNOW.Notary")

class QuizNotary:
    def __init__(self, output_dir: Optional[str] = None):
        if output_dir:
            self.output_dir = output_dir
        else:
            self.output_dir = os.path.join(get_base_dir(), "sessions")
        os.makedirs(self.output_dir, exist_ok=True)
        self.current_session_id = f"session_{int(time.time())}"
        self.session_file = os.path.join(self.output_dir, f"{self.current_session_id}.json")
        self.records: List[Dict[str, Any]] = []

    def log_question_answer(
        self,
        question_number: int,
        question_summary: str,
        question_type: str,
        reasoning: str,
        selected_ids: List[int],
        selected_texts: List[str],
        confidence: Optional[float] = None
    ):
        record: Dict[str, Any] = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "question_number": question_number,
            "question_summary": question_summary,
            "question_type": question_type,
            "reasoning": reasoning,
            "selected_option_ids": selected_ids,
            "selected_option_texts": selected_texts,
            "confidence": confidence
        }
        self.records.append(record)
        self._flush_to_disk()
        logger.info(f"Notulensi tercatat untuk Soal #{question_number} -> Pilihan ID: {selected_ids}")

    def _flush_to_disk(self):
        tmp_file = f"{self.session_file}.tmp"
        try:
            session_data = {
                "session_id": self.current_session_id,
                "total_recorded": len(self.records),
                "records": self.records
            }
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_file, self.session_file)
        except Exception as e:
            if os.path.exists(tmp_file):
                try:
                    os.remove(tmp_file)
                except Exception:
                    pass
            logger.error(f"Gagal menyimpan file notulensi sesi: {e}")

    def export_markdown(self) -> str:
        md_path = os.path.join(self.output_dir, f"{self.current_session_id}.md")
        lines = [
            "# SeeNOW Quiz Notary Report",
            f"**Session ID:** `{self.current_session_id}`",
            f"**Generated at:** `{time.strftime('%Y-%m-%d %H:%M:%S')}`\n",
            "---\n"
        ]
        for r in self.records:
            lines.append(f"### Soal #{r['question_number']} ({r['question_type'].upper()})")
            lines.append(f"**Pertanyaan:** {r['question_summary']}")
            lines.append(f"**Jawaban Benar (Opsi ID):** `{r['selected_option_ids']}`")
            lines.append(f"**Teks Pilihan:** {r['selected_option_texts']}")
            lines.append(f"**Analisis / Bukti (Reasoning):**\n> {r['reasoning']}\n")
            lines.append("---\n")

        content = "\n".join(lines)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(content)
        return md_path
