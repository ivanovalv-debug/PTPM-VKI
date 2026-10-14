from src.abstrakt.user_interface import UserInterface

class ConsoleUserInterface(UserInterface):
    
    def get_triangle_sides(self) -> tuple[float, float, float]:
        a = float(input("Введите длину стороны A: "))
        b = float(input("Введите длину стороны B: "))
        c = float(input("Введите длину стороны C: "))
        return a, b, c