# question_manager.py

from utils import safe_load_json, safe_save_json, QUESTION_FILE
from models import Question


def load_all_questions():
    raw = safe_load_json(QUESTION_FILE)
    return [Question.from_dict(entry) for entry in raw]


def save_all_questions(question_list):
    data = [q.to_dict() for q in question_list]
    safe_save_json(QUESTION_FILE, data)


def add_question():
    questions = load_all_questions()

    qid = input("Enter question ID: ").strip()
    if any(q.id == qid for q in questions):
        print("Warning: Question ID already exists.")
        return

    text = input("Enter question text: ").strip()
    if not text:
        print("Warning: Question text cannot be empty.")
        return

    options = []
    for opt in ["A", "B", "C", "D"]:
        ans = input(f"Answer {opt}: ").strip()
        if not ans:
            print("Warning: Option cannot be empty.")
            return
        options.append(ans)

    correct = input("Correct option (A/B/C/D): ").strip().upper()
    if correct not in {"A", "B", "C", "D"}:
        print("Warning: Correct option must be A, B, C, or D.")
        return

    level = input("Difficulty (BIẾT / HIỂU / VẬN DỤNG THẤP / VẬN DỤNG CAO): ").strip().upper()
    if level not in Question.VALID_LEVELS:
        print("Warning: Invalid difficulty level.")
        return

    # `qid` stays a string here
    new_q = Question(qid, text, options, correct, level)
    questions.append(new_q)
    save_all_questions(questions)
    print("Question added successfully.")


def edit_question():
    questions = load_all_questions()
    if not questions:
        print("No questions to edit.")
        return

    print("\nExisting Questions:")
    for q in questions:
        # q.id is a string
        print(f"- ID: {q.id} | Level: {q.level} | Text: {q.text[:50]}...")

    qid = input("Enter ID of question to edit: ").strip()
    # Compare string to string (no int conversion needed)
    target = next((q for q in questions if q.id == qid), None)
    if not target:
        print(f"Warning: No question with ID '{qid}'.")
        return

    print("Leave blank to keep existing value.")
    new_text = input(f"New text (current: {target.text}): ").strip()
    if new_text:
        target.text = new_text

    for idx, opt in enumerate(["A", "B", "C", "D"]):
        new_opt = input(f"Option {opt} (current: {target.options[idx]}): ").strip()
        if new_opt:
            target.options[idx] = new_opt

    new_correct = input(f"Correct option (current: {target.correct_option}): ").strip().upper()
    if new_correct:
        if new_correct in {"A", "B", "C", "D"}:
            target.correct_option = new_correct
        else:
            print("Warning: Invalid correct option; keeping old value.")

    new_level = input(f"Difficulty (current: {target.level}): ").strip().upper()
    if new_level:
        if new_level in Question.VALID_LEVELS:
            target.level = new_level
        else:
            print("Warning: Invalid level; keeping old value.")

    save_all_questions(questions)
    print("Question updated successfully.")


def remove_question():
    questions = load_all_questions()
    if not questions:
        print("No questions to remove.")
        return

    print("\nExisting Questions:")
    for q in questions:
        print(f"- ID: {q.id} | Text: {q.text[:50]}...")

    qid = input("Enter ID of question to delete: ").strip()
    new_list = [q for q in questions if q.id != qid]
    if len(new_list) == len(questions):
        print(f"Warning: No question with ID '{qid}'.")
        return

    save_all_questions(new_list)
    print(f"Question '{qid}' removed successfully.")


def get_questions_by_level():
    """
    Returns a dict: { level_str: [Question,...] }
    """
    questions = load_all_questions()
    result = {lvl: [] for lvl in Question.VALID_LEVELS}
    for q in questions:
        result.setdefault(q.level, []).append(q)
    return result