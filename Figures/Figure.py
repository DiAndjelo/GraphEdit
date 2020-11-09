from abc import ABC, abstractmethod

from PyQt5.QtGui import QColor, QPainter


class Figure(ABC):
    """
    Абстрактный класс каждого объекта
    """
    @abstractmethod
    def __init__(self):
        pass

    # ================================================== Movement ================================================== #

    @abstractmethod
    def move(self, x: int, y: int) -> None:
        """
        Метод для проверки положения мыши для начала передвижения объекта
        """
        pass

    @abstractmethod
    def stop_moving(self) -> None:
        """
        Прерывание передвижения объекта
        """
        pass

    @abstractmethod
    def move_or_deselect(self, x: int, y: int) -> None:
        """
        Проверка для продолжения движения. Если в точке для движения - двигаемся, иначе - деселект
        """
        pass

    @abstractmethod
    def transport(self, x: int, y: int) -> None:
        """
        Начало передвижения и вызов transport_center
        """
        pass

    @abstractmethod
    def transport_center(self, dx: int, dy: int) -> None:
        """
        Непосредственное передвижение объекта
        """
        pass

    # ============================================ Checkers and setters ============================================ #

    @abstractmethod
    def in_bounds(self, x: int, y: int) -> bool:
        """
        Проверка положения мыши на то, что она внутри редактора
        """
        pass

    @abstractmethod
    def is_coord_on_figure(self, x: int, y: int) -> bool:
        """
        Проверка, что маркер находится на фигуре
        """
        pass

    @abstractmethod
    def set_central_coord(self) -> None:
        """
        Установка центрального маркера
        """
        pass

    @abstractmethod
    def set_start_coord(self, x1: int, y2: int) -> None:
        """
        Установка начального маркера
        """
        pass

    @abstractmethod
    def set_end_coord(self, x2: int, y2: int) -> None:
        """
        Установка конечного маркера
        """
        pass

    @abstractmethod
    def set_thickness(self, thickness: int) -> None:
        """
        Установка толщины линии объекта
        """
        pass

    @abstractmethod
    def set_color(self, color: QColor) -> None:
        """
        Установка цвета фигуры
        """
        pass

    # =================================================== Actions ================================================== #

    @abstractmethod
    def select(self) -> None:
        """
        Выбор фигуры
        """
        pass

    @abstractmethod
    def deselect(self) -> None:
        """
        Снятие выбора фигуры
        """
        pass

    @abstractmethod
    def add_figure(self, figure) -> None:
        """
        Добавление объекта в массив для слияния объектов
        """
        pass

    @abstractmethod
    def fill(self, color: QColor) -> None:
        """
        Заполнение фигуры цветом
        """
        pass

    @abstractmethod
    def draw_selected(self, painter: QPainter) -> None:
        """
        Рисует маркеры. Для слитых объектов
        """
        pass

    @abstractmethod
    def draw(self, painter: QPainter, color: QColor, thickness: int, x: int, y: int) -> None:
        """
        Рисует фигуру.
        """
        pass
