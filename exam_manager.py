# exam_manager.py

import random
import math
from utils import (
    safe_load_json,
    safe_save_json,
    EXAM_FILE,
    ANSWER_FILE,
    parse_answers
)
from models import Question


def load_all_exams():
    return safe_load_json(EXAM_FILE)


def save_all_exams(exams):
    safe_save_json(EXAM_FILE, exams)


def load_all_answers():
    return safe_load_json(ANSWER_FILE)


def save_all_answers(ans_list):
    safe_save_json(ANSWER_FILE, ans_list)


def create_exam():
    """
    Admin function: specify an exam ID and how many questions at each level.
    Randomly pick from available questions, write an .txt file, and record in exam.json.
    """
    exams = load_all_exams()
    existing_ids = {e["ID"] for e in exams}

    exam_id = input("Enter new Exam ID: ").strip()
    if exam_id in existing_ids:
        print("Warning: Exam ID already exists.")
        return

    # Load questions by level
    from question_manager import get_questions_by_level
    by_level = get_questions_by_level()

    # Show how many questions are available at each level
    for lvl in Question.VALID_LEVELS:
        total = len(by_level.get(lvl, []))
        print(f"Level '{lvl}': {total} available questions.")

    cnt_easy = input("Number of 'BIẾT' questions: ").strip()
    cnt_medium = input("Number of 'HIỂU' questions: ").strip()
    cnt_low_app = input("Number of 'VẬN DỤNG THẤP' questions: ").strip()
    cnt_high_app = input("Number of 'VẬN DỤNG CAO' questions: ").strip()

    if not all(x.isdigit() for x in [cnt_easy, cnt_medium, cnt_low_app, cnt_high_app]):
        print("Warning: All must be non-negative integers.")
        return

    cnt_easy, cnt_medium, cnt_low_app, cnt_high_app = map(int, [cnt_easy, cnt_medium, cnt_low_app, cnt_high_app])

    # Check availability
    if (cnt_easy > len(by_level["BIẾT"])
        or cnt_medium > len(by_level["HIỂU"])
        or cnt_low_app > len(by_level["VẬN DỤNG THẤP"])
        or cnt_high_app > len(by_level["VẬN DỤNG CAO"])):
        print("Warning: Requested number exceeds available questions.")
        return

    # Random selection of question IDs
    sel_ids = []
    sel_ids += random.sample([q.id for q in by_level["BIẾT"]], cnt_easy)
    sel_ids += random.sample([q.id for q in by_level["HIỂU"]], cnt_medium)
    sel_ids += random.sample([q.id for q in by_level["VẬN DỤNG THẤP"]], cnt_low_app)
    sel_ids += random.sample([q.id for q in by_level["VẬN DỤNG CAO"]], cnt_high_app)

    # Build lookup of all questions by ID
    all_qs = {q.id: q for q in (by_level["BIẾT"] + by_level["HIỂU"]
                                 + by_level["VẬN DỤNG THẤP"] + by_level["VẬN DỤNG CAO"])}

    # Create exam text file
    filename = f"{exam_id}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for idx, qid in enumerate(sel_ids, start=1):
                q = all_qs[qid]
                f.write(f"{idx}. {q.text}\n")
                f.write(f"A. {q.options[0]}\n")
                f.write(f"B. {q.options[1]}\n")
                f.write(f"C. {q.options[2]}\n")
                f.write(f"D. {q.options[3]}\n\n")
    except IOError as e:
        print(f"Error: Cannot create exam file '{filename}': {e}")
        return

    # Build the list of correct answers in order
    correct_list = [all_qs[qid].correct_option for qid in sel_ids]

    # Record in exam.json
    exams.append({
        "ID": exam_id,
        "file": filename,
        "rightanswer": correct_list
    })
    save_all_exams(exams)
    print(f"Exam '{exam_id}' created, file: {filename}.")


def take_exam(current_user):
    """
    Student function: prompt for exam ID, load .txt, accept answers, and save to answers.json.
    """
    exams = load_all_exams()
    if not exams:
        print("No exams available.")
        return

    print("\nAvailable exams:")
    for e in exams:
        print(f"- {e['ID']}")

    exam_id = input("Enter Exam ID to take: ").strip()
    chosen = next((e for e in exams if e["ID"] == exam_id), None)
    if not chosen:
        print("Warning: No such exam.")
        return

    # Display exam content
    try:
        with open(chosen["file"], "r", encoding="utf-8") as f:
            content = f.read()
            print("\n" + content)
    except IOError:
        print(f"Error: Cannot open file '{chosen['file']}'.")
        return

    total_q = len(chosen["rightanswer"])
    ans_input = input(f"Enter your answers (format '1.A 2.B ...', total {total_q}): ").strip()
    answers = parse_answers(ans_input, total_q)

    all_answers = load_all_answers()
    record = {
        "ID": exam_id,                # exam identifier
        "username": current_user.username,
        "answer": answers,            # list of answers or None
        "score": None                 # to be filled later
    }
    all_answers.append(record)
    save_all_answers(all_answers)
    print("Your answers have been submitted. Await grading.")


def grade_exams():
    """
    Admin function: grade all ungraded exams. The resulting score is a float with two decimal places.
    """
    all_answers = load_all_answers()
    exams = load_all_exams()

    updated = False
    for entry in all_answers:
        if entry.get("score") is not None:
            continue  # already graded

        exam_id = entry["ID"]
        exam = next((e for e in exams if e["ID"] == exam_id), None)
        if not exam:
            print(f"Warning: Exam '{exam_id}' not found for record {entry}. Skipping.")
            continue

        correct_answers = exam.get("rightanswer", [])
        student_answers = entry.get("answer", [])

        if len(student_answers) != len(correct_answers):
            print(f"Warning: Mismatch answer count for {entry['username']} on Exam '{exam_id}'. Skipping.")
            continue

        correct_count = sum(
            1 for i in range(len(correct_answers))
            if student_answers[i] == correct_answers[i]
        )
        raw_score = (correct_count / len(correct_answers)) * 10

        # Round to two decimals using math: .5 and above rounds up
        rounded = math.floor(raw_score * 100 + 0.5) / 100

        entry["score"] = rounded
        updated = True
        print(f"Graded: {entry['username']} | Exam '{exam_id}' → {rounded:.2f}/10")

    if updated:
        save_all_answers(all_answers)
    else:
        print("No ungraded exams found.")


def generate_report():
    """
    Admin function: for a given Exam ID, produce:
      - highest score
      - lowest score
      - average score
      - variance
      - histogram (based on integer buckets, using math‐style rounding)
    """
    answers = load_all_answers()
    exams = load_all_exams()

    exam_id = input("Enter Exam ID for report: ").strip()
    exam = next((e for e in exams if e["ID"] == exam_id), None)
    if not exam:
        print("Warning: No such exam.")
        return

    # Filter only entries that match this exam and have a numeric score
    exam_records = [
        r for r in answers
        if r.get("ID") == exam_id and isinstance(r.get("score"), (int, float))
    ]
    if not exam_records:
        print("No graded records for this exam.")
        return

    # Collect scores as floats
    scores = [float(r["score"]) for r in exam_records]
    n = len(scores)
    mx = max(scores)
    mn = min(scores)
    avg = sum(scores) / n
    var = sum((x - avg) ** 2 for x in scores) / n

    print(f"\nReport for Exam '{exam_id}':")
    print(f"- Number of students: {n}")
    print(f"- Highest score: {mx:.2f}")
    print(f"- Lowest score: {mn:.2f}")
    print(f"- Average score: {avg:.2f}")
    print(f"- Variance: {var:.2f}\n")

    # Build a histogram: first convert each float into the nearest integer bucket
    hist_counts = [0] * 11  # index 0..10
    for s in scores:
        # Convert to nearest integer using math: .5 and above → next integer
        bucket = math.floor(s + 0.5)
        if bucket < 0:
            bucket = 0
        elif bucket > 10:
            bucket = 10
        hist_counts[bucket] += 1

    print("Score Distribution:")
    for score_val, count in enumerate(hist_counts):
        bar = "█" * count
        print(f"{score_val:2d} | {bar} ({count})")


def view_student_scores(current_user):
    """
    Student: list all exams they have taken and show their score (or “Not yet graded”).
    """
    all_answers = load_all_answers()
    exams = load_all_exams()

    # Filter answers for this user
    user_records = [r for r in all_answers if r.get("username") == current_user.username]
    if not user_records:
        print("\nYou have not taken any exams yet.")
        return

    print(f"\nScores for '{current_user.username}':")
    for entry in user_records:
        eid = entry.get("ID")
        score = entry.get("score")

        exam_obj = next((e for e in exams if e["ID"] == eid), None)
        if exam_obj is None:
            exam_label = f"{eid} (exam no longer exists)"
        else:
            exam_label = eid

        if score is None:
            print(f"- Exam '{exam_label}': Not yet graded")
        else:
            print(f"- Exam '{exam_label}': {score:.2f}/10")