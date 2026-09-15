import logging
from logger import Logger
from triangle import TriangleAnalyzer


if __name__ == "__main__":
    
    Logger.setup()
    
    logging.info("=== Приложение запущено ===")

    analyzer = TriangleAnalyzer()

    test_cases = [
        ("3", "3", "3"),
        ("5", "5", "8"),
        ("3", "4", "5"),
        ("1", "2", "10"),
        ("-1", "5", "5"),
        ("abc", "5", "5"),
        ("0", "0", "0"),
    ]

    for i, (a, b, c) in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"Тест {i}: ({a}, {b}, {c})")
        result = analyzer.analyze(a, b, c)
        print(f"  Тип:         {result['type']}")
        print(f"  Координаты:  {result['coordinates']}")

    logging.info("=== Приложение завершено ===")