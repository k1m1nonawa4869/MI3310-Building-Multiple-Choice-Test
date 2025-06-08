# test/test_exam_manager.py
import pytest, json
from controllers.exam_manager import load_all_exams, save_all_exams, take_exam

def test_load_and_save_exams(temp_data_dir):
    assert load_all_exams() == []
    entry = {"ID":"X","file":"X.txt","rightanswer":["A"]}
    save_all_exams([entry])
    assert load_all_exams() == [entry]

def test_take_exam_no_exams(capsys):
    # monkeypatch load_all_exams to return empty
    import controllers.exam_manager as em
    em.load_all_exams = lambda: []
    take_exam(None)
    out = capsys.readouterr().out
    assert "No exams available." in out
