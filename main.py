# main.py

import sys

# Import controller functions from controllers/
from controllers.user_manager import register_user, login_user, approve_users
from controllers.question_manager import add_question, edit_question, remove_question
from controllers.exam_manager import create_exam, take_exam, grade_exams, generate_report, view_student_scores

# Import our new “view” helpers (menu‐printing + input) from views/cli.py
from views.cli import (
    show_main_menu,
    show_admin_menu,
    show_manage_questions_menu,
    show_manage_exams_menu,
    show_student_menu
)


def main():
    while True:
        # Show the top‐level menu and get choice
        choice = show_main_menu()

        if choice == "1":
            # Register new user
            register_user()

        elif choice == "2":
            # Attempt to log in
            user = login_user()
            if not user:
                # login_user() prints its own error/“not verified” messages
                continue

            # If login succeeded, dispatch to Admin vs. Student
            if user.admin:
                run_admin_flow(user)
            else:
                run_student_flow(user)

        elif choice == "3":
            # Exit
            print("Goodbye!")
            sys.exit(0)

        else:
            print("Invalid selection. Please choose 1-3.")


def run_admin_flow(current_admin):
    """
    Repeatedly show admin menu until they log out.
    """
    while True:
        choice = show_admin_menu()

        if choice == "1":
            # Approve any pending users
            approve_users(current_admin)

        elif choice == "2":
            # Enter Manage Questions sub‐menu
            run_manage_questions_flow()

        elif choice == "3":
            # Enter Manage Exams sub‐menu
            run_manage_exams_flow()

        elif choice == "4":
            # Logout: return to top‐level main menu
            print("Logging out...")
            return

        else:
            print("Invalid selection. Please choose 1-4.")


def run_manage_questions_flow():
    """
    Loop inside “Manage Questions” until the user chooses “Back”.
    """
    while True:
        choice = show_manage_questions_menu()

        if choice == "1":
            add_question()
        elif choice == "2":
            edit_question()
        elif choice == "3":
            remove_question()
        elif choice == "4":
            return  # Go back to Admin menu
        else:
            print("Invalid selection. Please choose 1-4.")


def run_manage_exams_flow():
    """
    Loop inside “Manage Exams” until the user chooses “Back”.
    """
    while True:
        choice = show_manage_exams_menu()

        if choice == "1":
            create_exam()
        elif choice == "2":
            grade_exams()
        elif choice == "3":
            generate_report()
        elif choice == "4":
            return  # Go back to Admin menu
        else:
            print("Invalid selection. Please choose 1-4.")


def run_student_flow(current_student):
    """
    Repeatedly show student menu until they log out.
    """
    while True:
        choice = show_student_menu()

        if choice == "1":
            take_exam(current_student)
        elif choice == "2":
            view_student_scores(current_student)
        elif choice == "3":
            print("Logging out...")
            return
        else:
            print("Invalid selection. Please choose 1-3.")


if __name__ == "__main__":
    main()
