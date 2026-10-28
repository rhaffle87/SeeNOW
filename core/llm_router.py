# core/llm_router.py
import re
import time
import json
import logging
from typing import Dict, Any, Optional
from openai import OpenAI
from pydantic import BaseModel, Field

logger = logging.getLogger("SeeNOW.LLM")

def extract_json_from_text(raw: str) -> Dict[str, Any]:
    text = raw.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()
    else:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            text = text[start:end+1]
    return json.loads(text)

class QuizResponseSchema(BaseModel):
    question_summary: str = Field(description="Ringkasan teks pertanyaan")
    question_type: str = Field(description="Tipe: single_choice, multi_choice, true_false")
    reasoning: str = Field(description="Bukti langkah ringkas maksimal 2 kalimat")
    correct_option_ids: list[int] = Field(description="ID opsi yang benar")
    correct_option_texts: list[str] = Field(description="Teks opsi")
    next_button_id: Optional[int] = Field(default=None, description="ID tombol Next")
    is_final_submit: bool = Field(default=False, description="True jika tombol submit/selesai")

SEENOW_FAST_SYSTEM_PROMPT = """You are SeeNOW, an ultra-fast high-accuracy exam solver.
Rules:
1. Examine the screenshot and [ID] elements list.
2. Under 'reasoning': give concise analytical proof (1-2 sentences maximum).
3. Under 'correct_option_ids': list the integer ID(s) matching the correct option badge.
4. Under 'next_button_id': provide the ID of the 'Next' / 'Selanjutnya' button (or null if on final question).
5. If only 'Submit' / 'Finish' / 'Kirim' is present without Next, set 'is_final_submit': true and 'next_button_id': null.
6. Output strictly valid JSON matching this schema:
{
  "question_summary": "string",
  "question_type": "single_choice" | "multi_choice" | "true_false",
  "reasoning": "proof in 1-2 sentences",
  "correct_option_ids": [number],
  "correct_option_texts": ["string"],
  "next_button_id": number | null,
  "is_final_submit": boolean
}"""

class LLMRouterClient:
    def __init__(self, config_manager):
        self.config = config_manager
        self.client: Optional[OpenAI] = None
        self._init_client()

    def _init_client(self):
        base_url = self.config.get("router_base_url", "http://localhost:20128/v1")
        api_key = self.config.get("router_api_key", "").strip()
        timeout_sec = float(self.config.get("request_timeout_sec", 25))

        # Jika API key kosong, berikan dummy string agar SDK OpenAI tidak crash saat instansiasi
        effective_key = api_key if api_key else "EMPTY_KEY"

        self.client = OpenAI(
            base_url=base_url,
            api_key=effective_key,
            timeout=timeout_sec
        )

    def reload_config(self):
        self._init_client()

    def analyze_quiz(self, screenshot_b64: str, elements_summary: str) -> Dict[str, Any]:
        api_key = self.config.get("router_api_key", "").strip()
        if not api_key:
            raise ValueError("API Key 9router belum dikonfigurasi. Silakan isi API Key di tab Settings & 9router.")

        if not self.client:
            self._init_client()

        client: Any = self.client
        model_name = self.config.get("primary_vision_model", "ag/gemini-3.8-flash-high")
        fallback_name = self.config.get("fallback_vision_model", "ag/gemini-3.8-flash-high")
        max_retries = int(self.config.get("max_retries", 2))

        user_content: Any = [
            {
                "type": "text",
                "text": f"Options on screen:\n{elements_summary}\n\nSolve the question accurately. Return JSON."
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{screenshot_b64}"
                }
            }
        ]

        messages: Any = [
            {"role": "system", "content": SEENOW_FAST_SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ]

        for attempt in range(1, max_retries + 1):
            try:
                t0 = time.time()
                resp = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    response_format={"type": "json_object"},
                    max_tokens=350,
                    temperature=0.0
                )
                raw = resp.choices[0].message.content
                parsed = extract_json_from_text(raw)
                elapsed = round(time.time() - t0, 2)
                logger.info(f"Inferensi model {model_name} sukses ({elapsed}s).")
                return parsed
            except Exception as e:
                logger.warning(f"Percobaan {attempt}/{max_retries} model {model_name} gagal: {e}")
                if attempt == max_retries:
                    break
                time.sleep(0.4)

        if fallback_name and fallback_name != model_name:
            logger.info(f"Mengalihkan ke fallback model: {fallback_name}")
            t0 = time.time()
            resp = client.chat.completions.create(
                model=fallback_name,
                messages=messages,
                response_format={"type": "json_object"},
                max_tokens=350,
                temperature=0.0
            )
            raw = resp.choices[0].message.content
            parsed = extract_json_from_text(raw)
            elapsed = round(time.time() - t0, 2)
            logger.info(f"Inferensi fallback model {fallback_name} sukses ({elapsed}s).")
            return parsed

        raise RuntimeError(f"Gagal memperoleh respons JSON dari 9router setelah {max_retries} percobaan.")
