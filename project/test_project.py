import pytest
from unittest.mock import patch, MagicMock

from project import main


def test_main_calls_menu_init():
    with patch("project.Menu") as MockMenu:
        main()
        MockMenu.return_value.init.assert_called_once()


def test_main_creates_new_menu_instance():
    with patch("project.Menu") as MockMenu:
        main()
        MockMenu.assert_called_once_with()
