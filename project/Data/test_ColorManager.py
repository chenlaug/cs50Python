import pytest
from unittest.mock import patch
from colorama import Fore, Style
from Data.colorManager import Color, ColorManager


def test_print_returns_colored_string():
    result = ColorManager.print("hello", Color.RED)
    assert result == f"{Fore.RED}hello{Style.RESET_ALL}"


def test_print_all_colors():
    for color, fore in ColorManager._map.items():
        result = ColorManager.print("test", color)
        assert result == f"{fore}test{Style.RESET_ALL}"


def test_print_empty_string():
    result = ColorManager.print("", Color.GREEN)
    assert result == f"{Fore.GREEN}{Style.RESET_ALL}"


def test_input_default_color_is_yellow(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "typed")
    result = ColorManager.input("Enter: ")
    assert result == "typed"


def test_input_uses_correct_color(monkeypatch):
    captured = {}
    def fake_input(prompt):
        captured["prompt"] = prompt
        return "value"
    monkeypatch.setattr("builtins.input", fake_input)
    ColorManager.input("Enter: ", Color.CYAN)
    assert Fore.CYAN in captured["prompt"]
    assert "Enter: " in captured["prompt"]


def test_color_enum_values():
    assert Color.RED.value == "red"
    assert Color.GREEN.value == "green"
    assert Color.BLUE.value == "blue"
    assert Color.YELLOW.value == "yellow"
    assert Color.CYAN.value == "cyan"
    assert Color.MAGENTA.value == "magenta"


def test_color_enum_invalid():
    with pytest.raises(ValueError):
        Color("purple")
