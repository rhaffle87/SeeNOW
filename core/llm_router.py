# core/llm_router.py
import re
import time
import json
import random
import logging
from typing import Dict, Any, Optional, List
import httpx
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
    question_summary: str = Field(default="", description="Ringkasan teks pertanyaan")
    question_type: str = Field(default="single_choice", description="Tipe: single_choice, multi_choice, true_false")
    reasoning: str = Field(default="", description="Bukti langkah ringkas maksimal 1 kalimat")
    correct_option_ids: list[int] = Field(default_factory=list, description="ID opsi yang benar")
    correct_option_texts: list[str] = Field(default_factory=list, description="Teks opsi")
    next_button_id: Optional[int] = Field(default=None, description="ID tombol Next")
    is_final_submit: bool = Field(default=False, description="True jika tombol submit/selesai")

def validate_and_normalize_response(raw_dict: Dict[str, Any], elements: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    # Remap flexible key names if returned
    if "correct_ids" in raw_dict and "correct_option_ids" not in raw_dict:
        raw_dict["correct_option_ids"] = raw_dict["correct_ids"]
    if "next_id" in raw_dict and "next_button_id" not in raw_dict:
        raw_dict["next_button_id"] = raw_dict["next_id"]
    if "type" in raw_dict and "question_type" not in raw_dict:
        raw_dict["question_type"] = raw_dict["type"]
    if "reason" in raw_dict and "reasoning" not in raw_dict:
        raw_dict["reasoning"] = raw_dict["reason"]

    # Local zero-latency text extraction for correct options from DOM elements
    if elements and not raw_dict.get("correct_option_texts"):
        target_ids = set(raw_dict.get("correct_option_ids", []))
        opt_texts = [el.get("text", "") for el in elements if el.get("id") in target_ids and el.get("text")]
        raw_dict["correct_option_texts"] = opt_texts

    validated = QuizResponseSchema.model_validate(raw_dict)
    return validated.model_dump()

SEENOW_FAST_SYSTEM_PROMPT = """You are SeeNOW, an ultra-fast exam solver.
Task: Identify the correct option ID(s) and forward next button ID from the screen and options list.
Rules:
1. Closely inspect all network topologies, diagrams, tables, and question text in the screenshot alongside the [ID] options list. Elements marked [ALREADY_CHECKED] are currently selected.
2. Determine if pre-checked options are 100% correct.
3. 'question_summary': 2-5 words topic/keywords.
4. 'reasoning': ultra-concise proof (1 short sentence, max 12 words).
5. 'correct_option_ids': integer IDs of the options that SHOULD be selected.
6. 'next_button_id': integer ID of forward Next / Submit button. NEVER select Previous or question cards.
7. If final question ('Submit'/'Finish'/'Kirim'), set 'is_final_submit': true.
8. Output strictly valid JSON matching this schema:
{
  "question_summary": "string",
  "question_type": "single_choice" | "multi_choice" | "true_false",
  "reasoning": "short proof",
  "correct_option_ids": [number],
  "next_button_id": number | null,
  "is_final_submit": boolean
}"""

class LLMRouterClient:
    def __init__(self, config_manager):
        self.config = config_manager
        self.client: Optional[OpenAI] = None
        self.http_client: Optional[httpx.Client] = None
        self._init_client()

    def _init_client(self):
        base_url = self.config.get("router_base_url", "http://localhost:20128/v1")
        api_key = self.config.get("router_api_key", "").strip()
        timeout_sec = float(self.config.get("request_timeout_sec", 45))

        effective_key = api_key if api_key else "EMPTY_KEY"

        if self.http_client:
            try:
                self.http_client.close()
            except Exception:
                pass

        # High-performance persistent HTTP Client with Keep-Alive connection pooling
        self.http_client = httpx.Client(
            timeout=httpx.Timeout(connect=8.0, read=timeout_sec, write=8.0, pool=8.0),
            limits=httpx.Limits(max_keepalive_connections=25, max_connections=50, keepalive_expiry=120.0),
            transport=httpx.HTTPTransport(retries=1)
        )

        self.client = OpenAI(
            base_url=base_url,
            api_key=effective_key,
            http_client=self.http_client
        )

    def reload_config(self):
        self._init_client()

    def analyze_quiz(self, screenshot_b64: str, elements_summary: str, elements: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        api_key = self.config.get("router_api_key", "").strip()
        if not api_key:
            raise ValueError("API Key 9router belum dikonfigurasi. Silakan isi API Key di tab Settings & 9router.")

        if not self.client:
            self._init_client()

        client: Any = self.client
        model_name = self.config.get("primary_vision_model", "ag/gemini-3.8-flash-high")
        fallback_name = self.config.get("fallback_vision_model", "ag/gemini-3.8-flash-low")
        max_retries = int(self.config.get("max_retries", 3))

        user_content: Any = [
            {
                "type": "text",
                "text": f"Options on screen:\n{elements_summary}\n\nSolve accurately. Output JSON only."
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
                    max_tokens=300,
                    temperature=0.0
                )
                raw = resp.choices[0].message.content
                parsed = validate_and_normalize_response(extract_json_from_text(raw), elements=elements)
                elapsed = round(time.time() - t0, 2)
                logger.info(f"Inferensi model {model_name} sukses ({elapsed}s).")
                return parsed
            except Exception as e:
                logger.warning(f"Percobaan {attempt}/{max_retries} model {model_name} gagal: {e}")
                if attempt == max_retries:
                    break
                backoff = (0.4 * (2 ** (attempt - 1))) + random.uniform(0.05, 0.15)
                time.sleep(backoff)

        if fallback_name and fallback_name != model_name:
            logger.info(f"Mengalihkan ke fallback model: {fallback_name}")
            t0 = time.time()
            resp = client.chat.completions.create(
                model=fallback_name,
                messages=messages,
                response_format={"type": "json_object"},
                max_tokens=300,
                temperature=0.0
            )
            raw = resp.choices[0].message.content
            parsed = validate_and_normalize_response(extract_json_from_text(raw), elements=elements)
            elapsed = round(time.time() - t0, 2)
            logger.info(f"Inferensi fallback model {fallback_name} sukses ({elapsed}s).")
            return parsed

        raise RuntimeError(f"Gagal memperoleh respons JSON dari 9router setelah {max_retries} percobaan.")
