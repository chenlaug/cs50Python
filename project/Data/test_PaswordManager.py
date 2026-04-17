import pytest

from Data.credential import Credential
from Data.password_manager import PasswordManager


@pytest.fixture
def pm(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    manager = PasswordManager()
    manager.generation_key()
    manager.load_key()
    return manager


def test_add_credential_stores_credential(pm):
    pm.add_credential("site.com", "user", "pass")
    cred = pm.find_credential("site.com")
    assert isinstance(cred, Credential)
    assert cred.username == "user"


def test_add_credential_lowercases_site(pm):
    pm.add_credential("SITE.COM", "user", "pass")
    cred = pm.find_credential("site.com")
    assert cred.site == "site.com"


def test_add_credential_encrypts_password(pm):
    pm.add_credential("site.com", "user", "secret")
    cred = pm.find_credential("site.com")
    assert cred.password != "secret"


def test_find_credential_returns_credential(pm):
    pm.add_credential("example.com", "user1", "pass123")
    result = pm.find_credential("example.com")
    assert isinstance(result, Credential)
    assert result.username == "user1"


def test_find_credential_case_insensitive(pm):
    pm.add_credential("example.com", "user1", "pass123")
    result = pm.find_credential("EXAMPLE.COM")
    assert isinstance(result, Credential)


def test_find_credential_not_found_raises(pm):
    with pytest.raises(ValueError, match="No login information found"):
        pm.find_credential("unknown.com")


def test_show_credential_with_true_password(pm):
    pm.add_credential("site.com", "user", "mypassword")
    result = pm.show_credential_with_true_password("site.com")
    assert "mypassword" in result
    assert "user" in result
    assert "site.com" in result


def test_show_credential_not_found_raises(pm):
    with pytest.raises(ValueError):
        pm.show_credential_with_true_password("notfound.com")


def test_delete_credential_removes_it(pm):
    pm.add_credential("site.com", "user", "pass")
    msg = pm.delete_credential("site.com")
    assert "deleted" in msg.lower()
    with pytest.raises(ValueError):
        pm.find_credential("site.com")


def test_delete_credential_not_found_raises(pm):
    with pytest.raises(ValueError, match="No login information found"):
        pm.delete_credential("notfound.com")


def test_update_credential_site(pm):
    pm.add_credential("old.com", "user", "pass")
    result = pm.update_credential("old.com", "new.com", "user", "pass")
    assert "successfully" in result.lower()
    assert isinstance(pm.find_credential("new.com"), Credential)


def test_update_credential_username(pm):
    pm.add_credential("site.com", "olduser", "pass")
    pm.update_credential("site.com", "site.com", "newuser", "pass")
    cred = pm.find_credential("site.com")
    assert cred.username == "newuser"


def test_update_credential_password(pm):
    pm.add_credential("site.com", "user", "oldpass")
    pm.update_credential("site.com", "site.com", "user", "newpass")
    result = pm.show_credential_with_true_password("site.com")
    assert "newpass" in result


def test_update_credential_keeps_old_values_when_empty(pm):
    pm.add_credential("site.com", "user", "pass")
    pm.update_credential("site.com", "", "", "")
    cred = pm.find_credential("site.com")
    assert cred.username == "user"


def test_update_credential_not_found_raises(pm):
    with pytest.raises(ValueError):
        pm.update_credential("notfound.com", "new.com", "user", "pass")


def test_list_credentials_empty(pm):
    assert pm.list_credentials() == []


def test_list_credentials_returns_all(pm):
    pm.add_credential("a.com", "user1", "pass1")
    pm.add_credential("b.com", "user2", "pass2")
    creds = pm.list_credentials()
    assert len(creds) == 2
    assert all(isinstance(c, Credential) for c in creds)


def test_load_missing_file_raises(pm, tmp_path):
    with pytest.raises(FileNotFoundError):
        pm.load(tmp_path / "nonexistent.json")


def test_save_and_load(pm, tmp_path):
    pm.add_credential("abc.com", "user", "123")

    pm2 = PasswordManager()
    pm2.load_key()
    pm2.load(tmp_path / "passwords.json")

    assert any(c.site == "abc.com" for c in pm2.credentials)


def test_load_restores_credentials(pm, tmp_path):
    pm.add_credential("x.com", "alice", "secret")
    pm.add_credential("y.com", "bob", "hunter2")

    pm2 = PasswordManager()
    pm2.load_key()
    pm2.load(tmp_path / "passwords.json")

    sites = [c.site for c in pm2.credentials]
    assert "x.com" in sites
    assert "y.com" in sites
