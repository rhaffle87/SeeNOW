# tests/test_notary.py
import os
import tempfile
from core.quiz_notary import QuizNotary

def test_quiz_notary_recording():
    with tempfile.TemporaryDirectory() as tmpdir:
        notary = QuizNotary(output_dir=tmpdir)

        notary.log_question_answer(
            question_number=1,
            question_summary="Berapa prefiks ringkasan yang tepat untuk 172.16.1.0/24 dan 172.16.2.0/24?",
            question_type="single_choice",
            reasoning="Subnet 172.16.0.0/22 mencakup rentang dari 172.16.0.0 hingga 172.16.3.255.",
            selected_ids=[2],
            selected_texts=["B. 172.16.0.0/22"],
            confidence=0.99
        )

        assert len(notary.records) == 1
        assert notary.records[0]["question_number"] == 1
        assert notary.records[0]["selected_option_ids"] == [2]

        # Test export markdown
        md_file = notary.export_markdown()
        assert os.path.exists(md_file)
        with open(md_file, "r", encoding="utf-8") as f:
            text = f.read()
            assert "SeeNOW Quiz Notary Report" in text
            assert "172.16.0.0/22" in text
