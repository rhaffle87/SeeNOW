# tests/test_schema.py
from core.llm_router import QuizResponseSchema, validate_and_normalize_response

def test_schema_valid():
    data = {
        "question_summary": "Subnet /24 question",
        "question_type": "single_choice",
        "reasoning": "254 usable hosts.",
        "correct_option_ids": [2],
        "correct_option_texts": ["B. 192.168.1.0/24"],
        "next_button_id": 4,
        "is_final_submit": False
    }
    schema = QuizResponseSchema(**data)
    assert schema.question_type == "single_choice"
    assert schema.correct_option_ids == [2]
    assert schema.is_final_submit is False

def test_schema_optional_next():
    data = {
        "question_summary": "Final Question",
        "question_type": "true_false",
        "reasoning": "Answer is True.",
        "correct_option_ids": [1],
        "correct_option_texts": ["True"],
        "next_button_id": None,
        "is_final_submit": True
    }
    schema = QuizResponseSchema(**data)
    assert schema.next_button_id is None
    assert schema.is_final_submit is True

def test_schema_normalize_partial_response():
    # Model returns minimal JSON without optional/default fields
    partial_data = {
        "question_summary": "Minimal Question",
        "correct_option_ids": [3]
    }
    normalized = validate_and_normalize_response(partial_data)
    assert normalized["question_summary"] == "Minimal Question"
    assert normalized["correct_option_ids"] == [3]
    assert normalized["question_type"] == "single_choice"
    assert normalized["reasoning"] == ""
    assert normalized["next_button_id"] is None
    assert normalized["is_final_submit"] is False
