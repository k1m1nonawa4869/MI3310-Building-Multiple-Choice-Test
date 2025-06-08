# test/conftest.py
import pytest, json, os
from pathlib import Path

@pytest.fixture(autouse=True)
def temp_data_dir(tmp_path, monkeypatch):
    """
    Create a temporary data/ directory structure:
      data/
        User.json
        questions.json
        exam.json
        answers.json
        test/
    And monkeypatch all file‐path constants in utils.py and in each controller.
    """
    base = tmp_path / "data"
    base.mkdir()

    # create empty JSON files
    for fname in ("User.json", "questions.json", "exam.json", "answers.json"):
        (base / fname).write_text("[]", encoding="utf-8")

    # create test/ subfolder for exam .txt files
    testdir = base / "test"
    testdir.mkdir()

    # monkeypatch utils constants
    import data.utils as utils
    monkeypatch.setattr(utils, "BASE_DIR", str(base))

    # monkeypatch controller‐specific file constants
    import controllers.user_manager as um
    monkeypatch.setattr(um, "USER_FILE", str(base / "User.json"))

    import controllers.question_manager as qm
    monkeypatch.setattr(qm, "QUESTION_FILE", str(base / "questions.json"))

    import controllers.exam_manager as em
    # JSON metadata
    monkeypatch.setattr(em, "EXAM_FILE", str(base / "exam.json"))
    monkeypatch.setattr(em, "ANSWER_FILE", str(base / "answers.json"))
    # Text files
    monkeypatch.setattr(em, "BASE_DIR_JSON", str(base))
    monkeypatch.setattr(em, "BASE_DIR_TXT", str(testdir))

    return base
