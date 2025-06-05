# user_manager.py

from utils import safe_load_json, safe_save_json, USER_FILE
from models import User


def load_all_users():
    raw = safe_load_json(USER_FILE)
    return [User.from_dict(entry) for entry in raw]


def save_all_users(user_list):
    data = [u.to_dict() for u in user_list]
    safe_save_json(USER_FILE, data)


def register_user():
    users = load_all_users()

    username = input("Enter new username: ").strip()
    if any(u.username == username for u in users):
        print("Warning: Username already exists.")
        return

    name = input("Enter your full name: ").strip()
    if not name:
        print("Warning: Name cannot be empty.")
        return

    # Use plain input() so you can see what you type
    password = input("Enter password: ").strip()
    confirm = input("Confirm password: ").strip()
    if password != confirm:
        print("Warning: Passwords do not match.")
        return

    # Create user with is_admin=False, verified=False
    new_user = User.create(username, password, name, admin=False)
    users.append(new_user)
    save_all_users(users)
    print("Registration successful! Awaiting admin approval.")


def login_user():
    users = load_all_users()

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    for u in users:
        if u.username == username and u.password == password:
            if not u.verified:
                print("Your account is not yet verified by an admin.")
                return None
            print(f"Welcome back, {u.name}!")  # now use u.name
            return u

    print("Invalid username or password.")
    return None


def approve_users(current_admin):
    if not current_admin.admin:
        print("Error: You do not have permission to approve users.")
        return

    users = load_all_users()
    pending = [u for u in users if not u.verified]

    if not pending:
        print("No users pending approval.")
        return

    print("\nPending approvals:")
    for idx, u in enumerate(pending, start=1):
        print(f"{idx}. {u.username} ({u.name})")

    choice = input("Enter number to approve (or 'q' to quit): ").strip()
    if choice.lower() == 'q':
        return

    if not choice.isdigit():
        print("Warning: Invalid selection.")
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(pending):
        print("Warning: Selection out of range.")
        return

    user_to_approve = pending[idx]
    for u in users:
        if u.username == user_to_approve.username:
            u.verified = True
            break

    save_all_users(users)
    print(f"User '{user_to_approve.username}' has been approved.")
