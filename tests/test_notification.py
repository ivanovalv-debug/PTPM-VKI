import sys
import os
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.email_notification import EmailNotificationService


class TestEmailNotification(unittest.TestCase):

    @patch('builtins.print')
    def test_notify_prints_message(self, mock_print):
        service = EmailNotificationService()
        service.notify("Тестовое уведомление")
        mock_print.assert_called_once_with("Отправка уведомления по электронной почте: Тестовое уведомление")