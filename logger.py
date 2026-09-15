import logging
import sys


class Logger:
    """Настройка сквозного логирования."""
    
    LOG_FORMAT = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def setup() -> None:
        """Настраивает вывод логов в консоль и файл app.log."""
        # Защита от дублирования хендлеров при повторном вызове
        if logging.root.handlers:
            return
            
        logging.basicConfig(
            level=logging.DEBUG,
            format=Logger.LOG_FORMAT,
            datefmt=Logger.DATE_FORMAT,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler("app.log", encoding="utf-8"),
            ],
        )
        logging.info("Логгер успешно сконфигурирован")