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
    site = "newsite.com"
    username = "user"
    password = "pass"
    pm.add_credential(site, username, password)
    assert isinstance(pm.find_credential(site), Credential)
    msg = pm.delete_credential(site)
    assert "deleted" in msg or "supprimé" in msg


def test_delete_credential_not_found(pm):
    msg = pm.delete_credential("notfound.com")
    assert "No login information found for the site:" in msg


def test_encrypt_decrypt_password(pm):
    original = "secret"
    encrypted = pm.encrypt_password(original)
    assert isinstance(encrypted, str)
    decrypted = pm.decrypt_password(encrypted)
    assert decrypted == original


def test_list_credentials(pm):
    creds = pm.list_credentials()
    assert isinstance(creds, list)
    assert all(isinstance(c, Credential) for c in creds)


def test_save_and_load(tmp_path):
    filepath = tmp_path / "credentials.json"

    pm1 = PasswordManager()
    pm1.generation_key()
    pm1.load_key()
    pm1.add_credential("abc.com", "user", "123")
    pm1.save(filepath)

    pm2 = PasswordManager()
    pm2.generation_key()
    pm2.load_key()
    pm2.load(filepath)

    assert any(c.site == "abc.com" for c in pm2.credentials)
