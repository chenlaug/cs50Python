import pytest
from Data.color_enum import Color

def test_color_enum_members():
    assert Color.RED.value == 1
    assert Color.GREEN.value == 2
    assert Color.BLUE.value == 3
    assert Color.YELLOW.value == 4
    assert Color.CYAN.value == 5
    assert Color.MAGENTA.value == 6

def test_color_enum_names():
    assert Color(1).name == "RED"
    assert Color(6).name == "MAGENTA"
    assert Color["CYAN"] == Color.CYAN

def test_color_enum_invalid():
    with pytest.raises(ValueError):
        Color(99)
