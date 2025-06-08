# views/cli_view.py

def show_main_menu():
    """
    Show the top‐level menu (Register / Login / Exit).
    Returns the string the user typed ("1", "2", or "3").
    """
    print("\n=== Welcome to the Test Management System ===")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Select option (1-3): ").strip()
    return choice


def show_admin_menu():
    """
    Show the Admin Menu (Approve Users / Manage Questions / Manage Exams / Logout).
    Returns the string the admin typed ("1", "2", "3", or "4").
    """
    print("\n--- Admin Menu ---")
    print("1. Approve Users")
    print("2. Manage Questions")
    print("3. Manage Exams")
    print("4. Logout")
    choice = input("Select option (1-4): ").strip()
    return choice


def show_manage_questions_menu():
    """
    Show the “Manage Questions” submenu (Add / Edit / Remove / Back).
    Returns the string the admin typed ("1", "2", "3", or "4").
    """
    print("\n  --- Manage Questions ---")
    print("  1. Add Question")
    print("  2. Edit Question")
    print("  3. Remove Question")
    print("  4. Back to Admin Menu")
    choice = input("  Select option (1-4): ").strip()
    return choice


def show_manage_exams_menu():
    """
    Show the “Manage Exams” submenu (Create / Grade / Report / Back).
    Returns the string the admin typed ("1", "2", "3", or "4").
    """
    print("\n  --- Manage Exams ---")
    print("  1. Create Exam")
    print("  2. Grade Exams")
    print("  3. Generate Exam Report")
    print("  4. Back to Admin Menu")
    choice = input("  Select option (1-4): ").strip()
    return choice


def show_student_menu():
    """
    Show the Student Menu (Take Exam / View My Scores / Logout).
    Returns the string the student typed ("1", "2", or "3").
    """
    print("\n--- Student Menu ---")
    print("1. Take Exam")
    print("2. View My Scores")
    print("3. Logout")
    choice = input("Select option (1-3): ").strip()
    return choice