# test/test_question_manager.py
import pytest
import json
from controllers.question_manager import (
    load_all_questions, save_all_questions,
    add_question, edit_question, remove_question,
    get_questions_by_level
)
from models.models import Question

def test_load_and_save_questions(temp_data_dir):
    qs = load_all_questions()
    assert qs == []
    q = Question("1", "Text", ["A","B","C","D"], "A", "BIẾT")
    qs.append(q)
    save_all_questions(qs)
    re = load_all_questions()
    assert len(re) == 1
    assert re[0].id == "1"

def test_get_questions_by_level(tmp_path, monkeypatch):
    # prepare two questions in the JSON
    ff = tmp_path / "questions.json"
    data = [
      {"ID":"1","question":"T1","answer":["A","B","C","D"],"rightanswer":"A","level":"BIẾT"},
      {"ID":"2","question":"T2","answer":["A","B","C","D"],"rightanswer":"B","level":"HIỂU"},
    ]
    ff.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    import controllers.question_manager as qm
    monkeypatch.setattr(qm, "QUESTION_FILE", str(ff))

    by_level = get_questions_by_level()
    assert len(by_level["BIẾT"]) == 1
    assert len(by_level["HIỂU"]) == 1

# you can similarly write tests for add/edit/remove_question by monkeypatching input()
