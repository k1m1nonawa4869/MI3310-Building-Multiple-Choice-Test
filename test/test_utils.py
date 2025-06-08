# test/test_utils.py
import pytest
from data.utils import parse_answers, safe_load_json, safe_save_json
import os, json

def test_parse_answers_basic():
    assert parse_answers("1.A 2.B", 2) == ["A", "B"]

def test_parse_answers_invalid_tokens(capsys):
    result = parse_answers("foo 1.C", 2)
    captured = capsys.readouterr()
    assert "not in 'num.letter' format" in captured.out
    assert result == [None, "C"]

def test_safe_load_and_save_json(tmp_path):
    f = tmp_path / "x.json"
    # empty file => load returns []
    assert safe_load_json(str(f)) == []
    # malformed JSON => also []
    f.write_text("not json")
    assert safe_load_json(str(f)) == []

    # save a list then load it back
    data = [{"a":1}, {"b":2}]
    safe_save_json(str(f), data)
    assert json.loads(f.read_text(encoding="utf-8")) == data
