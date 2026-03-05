import pytest

from Data.credential import Credential
from Data.password_manager import PasswordManager


@pytest.fixture
def pm():
    manager = PasswordManager()
    manager.generation_key()
    manager.load_key()
    return manager


def test_add_credential(pm):
    pm.add_credential("newsite.com", "newuser", "newpass")
    result = pm.find_credential("newsite.com")
    assert isinstance(result, Credential)
    assert result.site == "newsite.com"
    assert pm.decrypt_password(result.password) == "newpass"


def test_add_credential_lowercases_site(pm):
    pm.add_credential("NewSite.COM", "user", "pass")
    result = pm.find_credential("newsite.com")
    assert isinstance(result, Credential)


def test_find_credential_existing(pm):
    pm.add_credential("example.com", "user1", "pass123")
    result = pm.find_credential("example.com")
    assert isinstance(result, Credential)
    assert result.username == "user1"
    assert pm.decrypt_password(result.password) == "pass123"


def test_find_credential_not_found(pm):
    result = pm.find_credential("unknown.com")
    assert isinstance(result, str)
    assert "Identifier not found for the site:" in result


def test_delete_credential_existing(pm):
    pm.add_credential("newsite.com", "user", "pass")
    assert isinstance(pm.find_credential("newsite.com"), Credential)
    msg = pm.delete_credential("newsite.com")
    assert "deleted" in msg or "supprimé" in msg
    assert not isinstance(pm.find_credential("newsite.com"), Credential)


def test_delete_credential_not_found(pm):
    msg = pm.delete_credential("notfound.com")
    assert "No login information found for the site:" in msg


def test_encrypt_decrypt_password(pm):
    original = "secret"
    encrypted = pm.encrypt_password(original)
    assert isinstance(encrypted, str)
    assert encrypted != original
    decrypted = pm.decrypt_password(encrypted)
    assert decrypted == original


def test_list_credentials_empty(pm):
    assert pm.list_credentials() == []


def test_list_credentials(pm):
    pm.add_credential("a.com", "user1", "pass1")
    pm.add_credential("b.com", "user2", "pass2")
    creds = pm.list_credentials()
    assert isinstance(creds, list)
    assert len(creds) == 2
    assert all(isinstance(c, Credential) for c in creds)


def test_update_credential_site(pm):
    pm.add_credential("old.com", "user", "pass")
    result = pm.update_credential("old.com", "1", {"site": "new.com"})
    assert "successfully" in result
    assert isinstance(pm.find_credential("new.com"), Credential)


def test_update_credential_username(pm):
    pm.add_credential("site.com", "olduser", "pass")
    result = pm.update_credential("site.com", "2", {"username": "newuser"})
    assert "successfully" in result
    cred = pm.find_credential("site.com")
    assert cred.username == "newuser"


def test_update_credential_password(pm):
    pm.add_credential("site.com", "user", "oldpass")
    result = pm.update_credential("site.com", "3", {"password": "newpass"})
    assert "successfully" in result
    cred = pm.find_credential("site.com")
    assert pm.decrypt_password(cred.password) == "newpass"


def test_update_credential_all(pm):
    pm.add_credential("old.com", "olduser", "oldpass")
    result = pm.update_credential("old.com", "4", {
        "site": "new.com",
        "username": "newuser",
        "password": "newpass"
    })
    assert "successfully" in result
    cred = pm.find_credential("new.com")
    assert isinstance(cred, Credential)
    assert cred.username == "newuser"
    assert pm.decrypt_password(cred.password) == "newpass"


def test_update_credential_invalid_choice(pm):
    pm.add_credential("site.com", "user", "pass")
    result = pm.update_credential("site.com", "9", {})
    assert "Invalid" in result


def test_update_credential_not_found(pm):
    result = pm.update_credential("notfound.com", "1", {"site": "other.com"})
    assert "not found" in result.lower()


def test_show_credential_with_true_password(pm):
    pm.add_credential("site.com", "user", "mypassword")
    result = pm.show_credential_with_true_password("site.com")
    assert "mypassword" in result
    assert "user" in result
    assert "site.com" in result


def test_show_credential_with_true_password_not_found(pm):
    result = pm.show_credential_with_true_password("notfound.com")
    assert result == "Not found"


def test_get_decrypted_password(pm):
    pm.add_credential("site.com", "user", "secret")
    result = pm.get_decrypted_password("site.com")
    assert result == "secret"


def test_get_decrypted_password_not_found(pm):
    result = pm.get_decrypted_password("notfound.com")
    assert "not found" in result.lower() or "Identifier" in result


def test_save_and_load(tmp_path, pm):
    filepath = tmp_path / "credentials.json"
    pm.add_credential("abc.com", "user", "123")
    pm.save(filepath)

    pm2 = PasswordManager()
    pm2.generation_key()
    pm2.load_key()
    pm2.load(filepath)

    assert any(c.site == "abc.com" for c in pm2.credentials)


def test_load_missing_file(pm, tmp_path):
    filepath = tmp_path / "nonexistent.json"
    pm.load(filepath)
    assert pm.credentials == []
