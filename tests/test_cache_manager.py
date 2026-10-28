# tests/test_cache_manager.py
import os
import tempfile
from core.cache_manager import (
    QuestionCacheManager,
    compute_question_cache_key,
    normalize_text
)

def test_normalize_text():
    assert normalize_text("  Hello   World \n ") == "hello world"
    assert normalize_text("") == ""

def test_compute_cache_key_order_invariant():
    key1 = compute_question_cache_key("What is IPv4?", ["10.0.0.1", "192.168.1.1", "172.16.0.1"])
    # Shuffled options should generate identical cache key
    key2 = compute_question_cache_key("What is IPv4?", ["192.168.1.1", "172.16.0.1", "10.0.0.1"])
    assert key1 == key2

def test_cache_put_get_and_persistence():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_file = os.path.join(tmpdir, "question_cache.json")
        manager = QuestionCacheManager(cache_file=cache_file, max_entries=5)

        data = {
            "question_summary": "Sample Question",
            "question_type": "single_choice",
            "reasoning": "Simple proof",
            "correct_option_texts": ["Option B"],
            "next_button_id": 3,
            "is_final_submit": False
        }

        manager.put("key_123", data)
        retrieved = manager.get("key_123")
        assert retrieved is not None
        assert retrieved["question_summary"] == "Sample Question"

        # Verify disk persistence
        manager2 = QuestionCacheManager(cache_file=cache_file)
        assert manager2.get("key_123") is not None

def test_cache_lru_eviction():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_file = os.path.join(tmpdir, "question_cache.json")
        manager = QuestionCacheManager(cache_file=cache_file, max_entries=2)

        manager.put("k1", {"val": 1})
        manager.put("k2", {"val": 2})
        # Access k1 to make k2 oldest
        assert manager.get("k1") is not None

        # Add k3, which should evict k2
        manager.put("k3", {"val": 3})

        assert manager.get("k1") is not None
        assert manager.get("k2") is None
        assert manager.get("k3") is not None

def test_resolve_cached_options_shuffled():
    cached_entry = {
        "correct_option_texts": ["Option 192.168.1.1"],
        "next_button_id": None
    }

    # On new screen, options are shuffled: Option 192.168.1.1 is now [ID 4], Next is [ID 5]
    current_elements = [
        {"id": 1, "tag": "input", "role": "radio", "text": "Option 10.0.0.1"},
        {"id": 2, "tag": "input", "role": "radio", "text": "Option 172.16.0.1"},
        {"id": 3, "tag": "input", "role": "radio", "text": "Option 127.0.0.1"},
        {"id": 4, "tag": "input", "role": "radio", "text": "Option 192.168.1.1"},
        {"id": 5, "tag": "button", "role": "button", "text": "Next Question"}
    ]

    matched_ids, next_id = QuestionCacheManager.resolve_cached_options(cached_entry, current_elements)
    assert matched_ids == [4]
    assert next_id == 5
