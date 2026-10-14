import logging
from src.triangle import TriangleAnalyzer
from src.database import Database
from src.abstrakt.user_interface import UserInterface
from src.abstrakt.notification_service import NotificationService


class Controller:

    def __init__(
        self,
        ui: UserInterface,
        db: Database,
        service: NotificationService
    ):
        self.ui = ui
        self.db = db
        self.service = service
        self.analyzer = TriangleAnalyzer()
        self.logger = logging.getLogger(self.__class__.__name__)

    def process_triangle(self) -> dict:
        sides = self.ui.get_triangle_sides()
        a, b, c = sides
        
        a_str, b_str, c_str = str(a), str(b), str(c)

        cached = self.db.get_record(a, b, c)

        if cached:
            result = cached
        else:
            analysis = self.analyzer.analyze(a_str, b_str, c_str)
            
            msg = ""
            if analysis["type"] == "не треугольник":
                msg = "Нарушены условия существования треугольника"
            elif analysis["type"] == "":
                msg = "Некорректные входные данные"
                
            result = {"type": analysis["type"], "message": msg}
            self.db.add_record(a, b, c, result["type"], result["message"])

        notification_msg = f"Анализ треугольника ({a},{b},{c}): {result['type']}"
        self.service.notify(notification_msg)

        return result