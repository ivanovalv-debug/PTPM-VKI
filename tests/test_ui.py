import sys
import os
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Пробуем импортировать из console_ui.py (краткое название)
try:
    from src.console_ui import ConsoleUserInterface
except ImportError:
    # Если не нашли, пробуем полное название
    from src.console_user_interface import ConsoleUserInterface


class TestConsoleUserInterface(unittest.TestCase):

    @patch('builtins.input', side_effect=["3", "4", "5"])
    def test_get_triangle_sides_returns_tuple(self, mock_input):
        ui = ConsoleUserInterface()
        result = ui.get_triangle_sides()
        self.assertEqual(result, (3.0, 4.0, 5.0))