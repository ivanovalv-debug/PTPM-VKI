import sys
import os
import unittest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.controller import Controller
from src.database import Database
from src.abstrakt.user_interface import UserInterface
from src.abstrakt.notification_service import NotificationService


class TestControllerIntegration(unittest.TestCase):

    def setUp(self):
        self.db = Database(":memory:")
        self.mock_ui = MagicMock(spec=UserInterface)
        self.mock_service = MagicMock(spec=NotificationService)
        self.controller = Controller(self.mock_ui, self.db, self.mock_service)

    def test_new_triangle_saved_to_db(self):
        self.mock_ui.get_triangle_sides.return_value = (3.0, 3.0, 3.0)
        
        result = self.controller.process_triangle()
        
        self.assertEqual(result["type"], "равносторонний")
        cached = self.db.get_record(3.0, 3.0, 3.0)
        self.assertIsNotNone(cached)

    def test_cached_result_from_db(self):
        self.db.add_record(5.0, 5.0, 8.0, "равнобедренный", "")
        self.mock_ui.get_triangle_sides.return_value = (5.0, 5.0, 8.0)
        
        result = self.controller.process_triangle()
        
        self.assertEqual(result["type"], "равнобедренный")

    def test_notification_sent_after_processing(self):
        self.mock_ui.get_triangle_sides.return_value = (3.0, 4.0, 5.0)
        
        self.controller.process_triangle()
        
        self.mock_service.notify.assert_called_once()
        call_args = self.mock_service.notify.call_args[0][0]
        self.assertIn("разносторонний", call_args)

    def test_invalid_input_handling(self):
        self.mock_ui.get_triangle_sides.return_value = (0.0, 0.0, 0.0)
        
        result = self.controller.process_triangle()
        
        self.assertEqual(result["type"], "не треугольник")

    def test_ui_called_once(self):
        self.mock_ui.get_triangle_sides.return_value = (1.0, 2.0, 3.0)
        
        self.controller.process_triangle()
        
        self.assertEqual(self.mock_ui.get_triangle_sides.call_count, 1)


if __name__ == "__main__":
    unittest.main()