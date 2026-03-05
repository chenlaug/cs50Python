import pytest
from unittest.mock import patch

from project import print_color, input_color, generate_key_password_manager, use_menu
from Data.color_enum import Color
from Data.credential import Credential
from Data.password_manager import PasswordManager


@pytest.fixture
def pm():
    manager = PasswordManager()
    manager.generation_key()
    manager.load_key()
    return manager


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
def test_use_menu_add(mock_input, pm):
    with patch.object(pm, "save"):
        use_menu("1", pm)
    assert any(c.site == "mysite" for c in pm.credentials)


@patch("builtins.input", return_value="nonexistent.com")
def test_use_menu_search_not_found(mock_input, pm, capsys):
    use_menu("2", pm)
    captured = capsys.readouterr()
    assert "nonexistent.com" in captured.out or captured.out == ""


@patch("builtins.input", return_value="nonexistent.com")
def test_use_menu_search_with_true_password_not_found(mock_input, pm, capsys):
    use_menu("3", pm)
    captured = capsys.readouterr()
    assert "Not found" in captured.out


@patch("builtins.input", return_value="mysite")
def test_use_menu_delete(mock_input, pm, capsys):
    pm.add_credential("mysite", "user", "pass")
    use_menu("4", pm)
    captured = capsys.readouterr()
    assert "deleted" in captured.out or "mysite" in captured.out


def test_use_menu_list_empty(pm, capsys):
    use_menu("5", pm)
    captured = capsys.readouterr()
    assert "No credentials found." in captured.out


def test_use_menu_list_with_credentials(pm, capsys):
    pm.add_credential("a.com", "user", "pass")
    use_menu("5", pm)
    captured = capsys.readouterr()
    assert "a.com" in captured.out


@patch("builtins.input", side_effect=["mysite", "2", "newuser"])
def test_use_menu_update(mock_input, pm, capsys):
    pm.add_credential("mysite", "olduser", "pass")
    with patch.object(pm, "save"):
        use_menu("6", pm)
    cred = pm.find_credential("mysite")
    assert isinstance(cred, Credential)
    assert cred.username == "newuser"


@patch("builtins.input", return_value="notfound.com")
def test_use_menu_update_not_found(mock_input, pm, capsys):
    use_menu("6", pm)
    captured = capsys.readouterr()
    assert "notfound.com" in captured.out


def test_use_menu_invalid_command(pm):
    with pytest.raises(ValueError, match="Unknown command"):
        use_menu("invalid", pm)
