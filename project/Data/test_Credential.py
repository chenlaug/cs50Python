import pytest
from Data.credential import Credential


def test_init_and_getters():
    cred = Credential("example.com", "user1", "pass123")
    assert cred.site == "example.com"
    assert cred.username == "user1"
    assert cred.password == "pass123"


def test_site_lowercased():
    cred = Credential("GitHub.COM", "user", "pass")
    assert cred.site == "github.com"


def test_setters():
    cred = Credential("site", "user", "pass")
    cred.site = "NewSite.COM"
    cred.username = "newuser"
    cred.password = "newpass"
    assert cred.site == "newsite.com"
    assert cred.username == "newuser"
    assert cred.password == "newpass"


def test_site_empty_raises():
    with pytest.raises(ValueError):
        Credential("", "user", "pass")


def test_site_whitespace_raises():
    with pytest.raises(ValueError):
        Credential("   ", "user", "pass")


def test_username_empty_raises():
    with pytest.raises(ValueError):
        Credential("site.com", "", "pass")


def test_username_whitespace_raises():
    with pytest.raises(ValueError):
        Credential("site.com", "   ", "pass")


def test_password_empty_raises():
    with pytest.raises(ValueError):
        Credential("site.com", "user", "")


def test_password_whitespace_raises():
    with pytest.raises(ValueError):
        Credential("site.com", "user", "   ")


def test_to_dict():
    cred = Credential("example.com", "user1", "pass123")
    assert cred.to_dict() == {"site": "example.com", "username": "user1", "password": "pass123"}


def test_from_dict():
    data = {"site": "example.com", "username": "user1", "password": "pass123"}
    cred = Credential.from_dict(data)
    assert isinstance(cred, Credential)
    assert cred.site == "example.com"
    assert cred.username == "user1"
    assert cred.password == "pass123"


def test_str_method():
    cred = Credential("example.com", "user1", "pass123")
    assert str(cred) == "(site=example.com, username=user1, password=pass123)"
