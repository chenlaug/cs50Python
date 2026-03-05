import pytest
from Data.color_enum import Color


def test_color_enum_values():
    assert Color.RED.value == "red"
    assert Color.GREEN.value == "green"
    assert Color.BLUE.value == "blue"
    assert Color.YELLOW.value == "yellow"
    assert Color.CYAN.value == "cyan"
    assert Color.MAGENTA.value == "magenta"


def test_color_enum_names():
    assert Color["RED"] == Color.RED
    assert Color["CYAN"] == Color.CYAN
    assert Color["MAGENTA"] == Color.MAGENTA


def test_color_enum_all_members():
    members = [c.name for c in Color]
    assert set(members) == {"RED", "GREEN", "BLUE", "YELLOW", "CYAN", "MAGENTA"}


def test_color_enum_invalid():
    with pytest.raises(ValueError):
        Color("purple")
