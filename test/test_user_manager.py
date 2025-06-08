# test/test_user_manager.py
import pytest, json
from controllers.user_manager import load_all_users, save_all_users, login_user, register_user
from models.models import User

def test_load_and_save_users(temp_data_dir):
    # initially empty adult admin was inserted in conftest
    users = load_all_users()
    assert isinstance(users, list)
    # append a new user
    new = User.create("bob", "pw", "Bob")
    users.append(new)
    save_all_users(users)

    reloaded = load_all_users()
    assert any(u.username == "bob" and not u.verified for u in reloaded)

def test_login_and_register(monkeypatch, capsys):
    # register a fresh user
    inputs = iter(["alice", "Alice", "pw", "pw"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    register_user()
    out = capsys.readouterr().out
    assert "Registration successful" in out

    # try login before approval
    inputs = iter(["alice", "pw"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    user = login_user()
    assert user is None
    out = capsys.readouterr().out
    assert "not yet verified" in out

    # simulate approval
    all_users = load_all_users()
    for u in all_users:
        if u.username == "alice":
            u.verified = True
    save_all_users(all_users)

    # now login should succeed
    inputs = iter(["alice", "pw"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    user = login_user()
    # ensure login succeeded before checking its attributes
    assert user is not None, "Expected login_user() to return a User, got None"
    assert user.username == "alice"