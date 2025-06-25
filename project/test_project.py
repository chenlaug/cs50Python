import pytest
from unittest.mock import patch
from project import (
    print_color,
    input_color,
    generate_key_password_manager,
    use_menu
)
from Data.color_enum import Color
from Data.credential import Credential
from Data.password_manager import PasswordManager


def test_print_color_with_string():
    result = print_color("Test", Color.GREEN)
    assert "Test" in result
    assert result.startswith("\x1b")
    assert result.endswith("\x1b[0m")


def test_print_color_with_credential():
    cred = Credential("example.com", "user", "pass")
    result = print_color(str(cred), Color.CYAN)
    assert str(cred) in result


@patch("builtins.input", return_value="hello")
def test_input_color(mock_input):
    result = input_color("Enter something: ", Color.MAGENTA)
    assert result == "hello"
    mock_input.assert_called_once()


def test_generate_key_password_manager_creates_instance():
    pm = generate_key_password_manager()
    assert isinstance(pm, PasswordManager)
    assert hasattr(pm, "credentials")
    assert pm.key is not None
    assert pm.fernet is not None


@patch("builtins.input", side_effect=["mysite", "me", "mypass"])
def test_use_menu_add(monkeypatch):
    pm = PasswordManager()
    pm.generation_key()
    pm.load_key()

    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: None)
    use_menu("1", pm)

    assert any(c.site == "mysite" for c in pm.credentials)



@patch("builtins.input", return_value="nonexistent.com")
def test_use_menu_search(monkeypatch):
    pm = PasswordManager()
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: None)
    use_menu("2", pm) 


def test_use_menu_invalid_command():
    pm = PasswordManager()
    with pytest.raises(ValueError, match="Unknown command"):
        use_menu("invalid", pm)
