# tests/test_json_parser.py
from core.llm_router import extract_json_from_text

def test_extract_pure_json():
    raw = '{"question_summary": "Test Question", "correct_option_ids": [1]}'
    result = extract_json_from_text(raw)
    assert result["question_summary"] == "Test Question"
    assert result["correct_option_ids"] == [1]

def test_extract_markdown_fenced_json():
    raw = """
    Here is the answer:
    ```json
    {
      "question_summary": "Fenced Question",
      "correct_option_ids": [2, 3],
      "next_button_id": 5
    }
    ```
    Thank you.
    """
    result = extract_json_from_text(raw)
    assert result["question_summary"] == "Fenced Question"
    assert result["correct_option_ids"] == [2, 3]
    assert result["next_button_id"] == 5

def test_extract_mixed_text_json():
    raw = 'Analysis complete. Result: {"question_summary": "Embedded", "correct_option_ids": [4]} Hope this helps.'
    result = extract_json_from_text(raw)
    assert result["question_summary"] == "Embedded"
    assert result["correct_option_ids"] == [4]
