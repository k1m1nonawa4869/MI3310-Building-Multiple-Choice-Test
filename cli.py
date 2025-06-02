# cli.py

import sys
from user_manager import register_user, login_user, approve_users
from question_manager import add_question, edit_question, remove_question
from exam_manager import create_exam, take_exam, grade_exams, generate_report, view_student_scores


def manage_questions_menu():
    """
    Present the “Manage Questions” sub‐menu. All choices here are numeric.
    """
    while True:
        print("\n  --- Manage Questions ---")
        print("  1. Add Question")
        print("  2. Edit Question")
        print("  3. Remove Question")
        print("  4. Back to Admin Menu")

        choice = input("  Select option (1-4): ").strip()
        if choice == "1":
            add_question()
        elif choice == "2":
            edit_question()
        elif choice == "3":
            remove_question()
        elif choice == "4":
            return       # go back to Admin menu
        else:
            print("  Invalid selection. Please choose 1-4.")


def manage_exams_menu():
    """
    Present the “Manage Exams” sub‐menu. All choices here are numeric.
    """
    while True:
        print("\n  --- Manage Exams ---")
        print("  1. Create Exam")
        print("  2. Grade Exams")
        print("  3. Generate Exam Report")
        print("  4. Back to Admin Menu")

        choice = input("  Select option (1-4): ").strip()
        if choice == "1":
            create_exam()
        elif choice == "2":
            grade_exams()
        elif choice == "3":
            generate_report()
        elif choice == "4":
            return       # go back to Admin menu
        else:
            print("  Invalid selection. Please choose 1-4.")


def admin_menu(current_user):
    """
    Top-level Admin menu. Sub‐menus for “Manage Questions” (option 2)
    and “Manage Exams” (option 3) will call the functions above.
    """
    while True:
        print("\n--- Admin Menu ---")
        print("1. Approve Users")
        print("2. Manage Questions")
        print("3. Manage Exams")
        print("4. Logout")

        choice = input("Select option (1-4): ").strip()
        if choice == "1":
            approve_users(current_user)
        elif choice == "2":
            manage_questions_menu()
        elif choice == "3":
            manage_exams_menu()
        elif choice == "4":
            print("Logging out...")
            return
        else:
            print("Invalid selection. Please choose 1-4.")


def student_menu(current_user):
    """
    Updated Student Menu:
      1. Take Exam
      2. View My Scores
      3. Logout
    """
    while True:
        print("\n--- Student Menu ---")
        print("1. Take Exam")
        print("2. View My Scores")
        print("3. Logout")

        choice = input("Select option (1-3): ").strip()
        if choice == "1":
            take_exam(current_user)
        elif choice == "2":
            view_student_scores(current_user)
        elif choice == "3":
            print("Logging out...")
            return
        else:
            print("Invalid selection. Please choose 1-3.")


def main():
    print("=== Welcome to the Test Management System ===")
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Select option (1-3): ").strip()
        if choice == "1":
            register_user()
        elif choice == "2":
            user = login_user()
            if user:
                if user.admin:
                    admin_menu(user)
                else:
                    student_menu(user)
        elif choice == "3":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid selection. Please choose 1-3.")


if __name__ == "__main__":
    main()