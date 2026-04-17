import pytest
import sys
import hashlib
import os
from unittest.mock import patch, MagicMock

from Data.menu import Menu
from Data.credential import Credential
from Data.password_manager import PasswordManager


@pytest.fixture
def menu():
    return Menu()


@pytest.fixture
def pm(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    manager = PasswordManager()
    manager.generation_key()
    manager.load_key()
    return manager

def test_setup_master_password_creates_file(menu, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch("Data.menu.ColorManager.input", return_value="secret"):
        menu._Menu__setup_master_password()
    assert (tmp_path / "master.hash").exists()

def test_setup_master_password_file_has_salt_and_hash(menu, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch("Data.menu.ColorManager.input", return_value="secret"):
        menu._Menu__setup_master_password()
    data = (tmp_path / "master.hash").read_bytes()
    assert len(data) == 16 + 32  

def test_verify_master_password_correct(menu, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch("Data.menu.ColorManager.input", return_value="secret"):
        menu._Menu__setup_master_password()
    with patch("Data.menu.ColorManager.input", return_value="secret"):
        menu._Menu__verify_master_password() 

def test_verify_master_password_wrong_3_times_exits(menu, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch("Data.menu.ColorManager.input", return_value="secret"):
        menu._Menu__setup_master_password()
    with patch("Data.menu.ColorManager.input", return_value="wrong"):
        with pytest.raises(SystemExit) as exc:
            menu._Menu__verify_master_password()
    assert exc.value.code == 1

def test_check_master_password_first_run_calls_setup(menu, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch.object(menu, "_Menu__setup_master_password") as mock_setup:
        with patch.object(menu, "_Menu__verify_master_password") as mock_verify:
            menu._Menu__check_master_password()
    mock_setup.assert_called_once()
    mock_verify.assert_not_called()

def test_check_master_password_existing_calls_verify(menu, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch("Data.menu.ColorManager.input", return_value="secret"):
        menu._Menu__setup_master_password()
    with patch.object(menu, "_Menu__verify_master_password") as mock_verify:
        menu._Menu__check_master_password()
    mock_verify.assert_called_once()

def test_menu_prints_all_seven_options(menu, capsys):
    menu._Menu__menu()
    out = capsys.readouterr().out
    for i in range(1, 8):
        assert str(i) in out

def test_show_credentials_empty(menu, capsys):
    mock_pm = MagicMock()
    mock_pm.list_credentials.return_value = []
    menu._Menu__show_credentials(mock_pm)
    out = capsys.readouterr().out
    assert "No credentials found." in out

def test_show_credentials_with_data(menu, capsys):
    mock_pm = MagicMock()
    mock_pm.list_credentials.return_value = [
        Credential("site.com", "user", "pass")
    ]
    menu._Menu__show_credentials(mock_pm)
    out = capsys.readouterr().out
    assert "site.com" in out
    assert "user" in out

def test_generate_key_password_manager_returns_pm(menu, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "passwords.json").write_text("[]")
    pm = menu._Menu__generate_key_password_manager()
    assert isinstance(pm, PasswordManager)
    assert pm.key is not None
    assert pm.fernet is not None

def test_generate_key_password_manager_credentials_empty(menu, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "passwords.json").write_text("[]")
    pm = menu._Menu__generate_key_password_manager()
    assert pm.list_credentials() == []

def test_use_menu_command_1_adds_credential(menu, pm, capsys):
    with patch("Data.menu.ColorManager.input", side_effect=["site.com", "user", "pass"]):
        menu._Menu__use_menu(1, pm)
    assert any(c.site == "site.com" for c in pm.credentials)

def test_use_menu_command_1_prints_confirmation(menu, pm, capsys):
    with patch("Data.menu.ColorManager.input", side_effect=["site.com", "user", "pass"]):
        menu._Menu__use_menu(1, pm)
    out = capsys.readouterr().out
    assert "added" in out.lower()

def test_use_menu_command_2_found_shows_site(menu, capsys):
    mock_pm = MagicMock()
    mock_pm.find_credential.return_value = Credential("site.com", "user", "pass")
    with patch("Data.menu.ColorManager.input", return_value="site.com"):
        menu._Menu__use_menu(2, mock_pm)
    out = capsys.readouterr().out
    assert "site.com" in out

def test_use_menu_command_2_not_found_raises(menu):
    mock_pm = MagicMock()
    mock_pm.find_credential.side_effect = ValueError("No login information found")
    with patch("Data.menu.ColorManager.input", return_value="unknown.com"):
        with pytest.raises(ValueError):
            menu._Menu__use_menu(2, mock_pm)

def test_use_menu_command_3_shows_password(menu, capsys):
    mock_pm = MagicMock()
    mock_pm.show_credential_with_true_password.return_value = (
        "site.com, Username: user, Password: secret"
    )
    with patch("Data.menu.ColorManager.input", return_value="site.com"):
        menu._Menu__use_menu(3, mock_pm)
    out = capsys.readouterr().out
    assert "secret" in out

def test_use_menu_command_3_not_found_raises(menu):
    mock_pm = MagicMock()
    mock_pm.show_credential_with_true_password.side_effect = ValueError("No login information found")
    with patch("Data.menu.ColorManager.input", return_value="notfound.com"):
        with pytest.raises(ValueError):
            menu._Menu__use_menu(3, mock_pm)

def test_use_menu_command_4_deletes_credential(menu, pm, capsys):
    pm.add_credential("site.com", "user", "pass")
    with patch("Data.menu.ColorManager.input", return_value="site.com"):
        menu._Menu__use_menu(4, pm)
    with pytest.raises(ValueError):
        pm.find_credential("site.com")

def test_use_menu_command_4_not_found_raises(menu):
    mock_pm = MagicMock()
    mock_pm.delete_credential.side_effect = ValueError("No login information found")
    with patch("Data.menu.ColorManager.input", return_value="notfound.com"):
        with pytest.raises(ValueError):
            menu._Menu__use_menu(4, mock_pm)

def test_use_menu_command_5_empty(menu, capsys):
    mock_pm = MagicMock()
    mock_pm.list_credentials.return_value = []
    menu._Menu__use_menu(5, mock_pm)
    out = capsys.readouterr().out
    assert "No credentials found." in out

def test_use_menu_command_5_with_data(menu, pm, capsys):
    pm.add_credential("a.com", "user1", "pass1")
    pm.add_credential("b.com", "user2", "pass2")
    menu._Menu__use_menu(5, pm)
    out = capsys.readouterr().out
    assert "a.com" in out
    assert "b.com" in out

def test_use_menu_command_6_updates_credential(menu, pm):
    pm.add_credential("old.com", "user", "pass")
    with patch("Data.menu.ColorManager.input", side_effect=["old.com", "new.com", "newuser", "newpass"]):
        menu._Menu__use_menu(6, pm)
    cred = pm.find_credential("new.com")
    assert cred.username == "newuser"


def test_use_menu_command_6_not_found_raises(menu):
    mock_pm = MagicMock()
    mock_pm.update_credential.side_effect = ValueError("No login information found")
    with patch("Data.menu.ColorManager.input", side_effect=["notfound.com", "x.com", "u", "p"]):
        with pytest.raises(ValueError):
            menu._Menu__use_menu(6, mock_pm)

def test_use_menu_command_7_exits_with_code_0(menu):
    with pytest.raises(SystemExit) as exc:
        menu._Menu__use_menu(7, MagicMock())
    assert exc.value.code == 0

def test_use_menu_invalid_command_raises_value_error(menu):
    with pytest.raises(ValueError, match="Invalid command"):
        menu._Menu__use_menu(99, MagicMock())
