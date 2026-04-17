from enum import Enum
from colorama import Fore, Style


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    CYAN = "cyan"
    MAGENTA = "magenta"


class ColorManager:
    _map = {
        Color.RED: Fore.RED,
        Color.GREEN: Fore.GREEN,
        Color.BLUE: Fore.BLUE,
        Color.YELLOW: Fore.YELLOW,
        Color.CYAN: Fore.CYAN,
        Color.MAGENTA: Fore.MAGENTA,
    }

    @classmethod
    def print(cls, txt: str, color: Color) -> str:
        return f"{cls._map.get(color)}{txt}{Style.RESET_ALL}"

    @classmethod
    def input(cls, txt: str, color: Color = Color.YELLOW) -> str:
        return input(f"{cls._map.get(color)}{txt}{Style.RESET_ALL}")
