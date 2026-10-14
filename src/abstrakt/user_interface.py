from abc import ABC, abstractmethod

class UserInterface(ABC):
    @abstractmethod
    def get_triangle_sides(self) -> tuple[float, float, float]:
        pass