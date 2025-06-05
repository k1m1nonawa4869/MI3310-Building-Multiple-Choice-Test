# utils.py

import json
import os


# BASE_DIR is now the folder where this file lives (i.e., "<project_root>/data")
BASE_DIR = os.path.dirname(__file__)

# Point directly at each JSON file inside data/
USER_FILE     = os.path.join(BASE_DIR, "User.json")
QUESTION_FILE = os.path.join(BASE_DIR, "questions.json")
EXAM_FILE     = os.path.join(BASE_DIR, "exam.json")
ANSWER_FILE   = os.path.join(BASE_DIR, "answers.json")

def safe_load_json(path):
    """
    Load a JSON file, returning an empty list if the file does not exist or is invalid.
    """
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print(f"Warning: Failed to load or parse '{path}'. Starting with empty list.")
        return []


def safe_save_json(path, data):
    """
    Save `data` to `path` as JSON. Writes to a temporary file first and then replaces.
    """
    temp_path = path + ".tmp"
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(temp_path, path)
    except IOError as e:
        print(f"Error: Could not write to '{path}': {e}")


def parse_answers(input_str, total_questions):
    """
    Parse a string like "1.A 2.B 5.D" into a list of answers of length `total_questions`.
    Returns a list where each entry is "A"/"B"/"C"/"D" or None if unanswered/malformed.
    """
    tokens = input_str.strip().split()
    answers = [None] * total_questions

    for token in tokens:
        try:
            question_part, answer_part = token.split(".")
            idx = int(question_part) - 1
            ans = answer_part.strip().upper()
            if idx < 0 or idx >= total_questions:
                print(f"Warning: Question number {question_part} is out of range.")
                continue
            if ans not in {"A", "B", "C", "D"}:
                print(f"Warning: Answer '{ans}' is not one of A/B/C/D.")
                continue
            answers[idx] = ans
        except ValueError:
            print(f"Warning: Token '{token}' is not in 'num.letter' format.")
            continue

    return answers


def round_scores(raw_scores):
    """
    Given a list of float scores (0..10), round each so that .5 always rounds UP.
    """
    rounded = []
    for x in raw_scores:
        try:
            val = float(x)
        except (ValueError, TypeError):
            rounded.append(0)
            continue

        integer_part = int(val // 1)
        fractional = val - integer_part
        if fractional < 0.5:
            rounded.append(integer_part)
        else:
            rounded.append(integer_part + 1)
    return rounded


def histogram(scores_list):
    """
    Given a list of integer (or float) scores 0..10, return a list of counts for each integer score.
    """
    counts = [0] * 11
    for s in scores_list:
        # Convert float to int if necessary, but only if it's exactly an integer
        if isinstance(s, float) and s.is_integer():
            s_int = int(s)
        elif isinstance(s, int):
            s_int = s
        else:
            print(f"Warning: Score '{s}' is not an integer between 0 and 10.")
            continue

        if 0 <= s_int <= 10:
            counts[s_int] += 1
        else:
            print(f"Warning: Score '{s_int}' is out of range 0..10.")
    return counts
