import logging


class TriangleValidator:
    """Валидация сторон и определение типа треугольника."""
    EPSILON = 1e-9

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def validate_and_classify(self, a_str: str, b_str: str, c_str: str) -> dict:
        self.logger.info(f"Валидация: A='{a_str}', B='{b_str}', C='{c_str}'")

        try:
            sides = [float(a_str), float(b_str), float(c_str)]
        except (ValueError, TypeError):
            self.logger.error("Некорректные данные (не числа)")
            return {"type": "", "error_code": -2}

        a, b, c = sides

        if any(s <= 0 for s in sides):
            self.logger.warning(f"Стороны <= 0: {sides}")
            return {"type": "не треугольник", "error_code": -1}

        if (a + b <= c) or (a + c <= b) or (b + c <= a):
            self.logger.warning(f"Нарушено неравенство треугольника: {sides}")
            return {"type": "не треугольник", "error_code": -1}

        eq_ab = abs(a - b) < self.EPSILON
        eq_bc = abs(b - c) < self.EPSILON
        eq_ac = abs(a - c) < self.EPSILON

        if eq_ab and eq_bc:
            t_type = "равносторонний"
        elif eq_ab or eq_bc or eq_ac:
            t_type = "равнобедренный"
        else:
            t_type = "разносторонний"

        self.logger.info(f"Тип определен: {t_type}")
        return {"type": t_type, "error_code": 0}


class CoordinateCalculator:
    """Расчет координат вершин для поля 100x100 px."""
    FIELD_SIZE = 100
    MARGIN = 5

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def calculate(self, a: float, b: float, c: float, error_code: int) -> list:
        if error_code == -2:
            return [(-2, -2)] * 3
        if error_code == -1:
            return [(-1, -1)] * 3

        max_side = max(a, b, c)
        scale = (self.FIELD_SIZE - 2 * self.MARGIN) / max_side if max_side > 0 else 1

        x1, y1 = self.MARGIN, self.MARGIN
        x2, y2 = int(x1 + a * scale), y1

        cos_angle = max(-1, min(1, (a**2 + b**2 - c**2) / (2 * a * b)))
        sin_angle = (1 - cos_angle ** 2) ** 0.5

        x3 = int(x1 + b * scale * cos_angle)
        y3 = int(y1 + b * scale * sin_angle)

        coords = [(x1, y1), (x2, y2), (x3, y3)]
        self.logger.debug(f"Координаты: {coords}")
        return coords


class TriangleAnalyzer:
    """Фасад: связывает валидатор и калькулятор."""

    def __init__(self):
        self.validator = TriangleValidator()
        self.calculator = CoordinateCalculator()
        self.logger = logging.getLogger(self.__class__.__name__)

    def analyze(self, a_str: str, b_str: str, c_str: str) -> dict:
        self.logger.info(f"Анализ запроса: ({a_str}, {b_str}, {c_str})")

        validation = self.validator.validate_and_classify(a_str, b_str, c_str)

        try:
            sides = [float(a_str), float(b_str), float(c_str)]
        except (ValueError, TypeError):
            sides = [0.0, 0.0, 0.0]

        coordinates = self.calculator.calculate(*sides, validation["error_code"])

        result = {
            "type": validation["type"],
            "coordinates": coordinates
        }
        self.logger.info(f"Результат анализа: {result}")
        return result