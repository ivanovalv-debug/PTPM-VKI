import logging
from src.logger import Logger
from src.controller import Controller
from src.console_ui import ConsoleUserInterface
from src.database import Database
from src.email_notification import EmailNotificationService


if __name__ == "__main__":
    Logger.setup()
    logging.info("=== Запуск лабораторной работы №3 ===")

    ui = ConsoleUserInterface()
    db = Database("database.db")
    service = EmailNotificationService()

    controller = Controller(ui, db, service)

    try:
        result = controller.process_triangle()
        print(f"\nРезультат: {result['type']}")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
    finally:
        db.close()
        logging.info("=== Работа завершена ===")