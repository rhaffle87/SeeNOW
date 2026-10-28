# tests/test_schema.py
from core.llm_router import QuizResponseSchema

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
