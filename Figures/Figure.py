from abc import ABC, abstractmethod


class Figure(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def stop_moving(self):
        pass

    @abstractmethod
    def move_or_deselect(self, x, y):
        pass

    @abstractmethod
    def move(self, x, y):
        pass

    @abstractmethod
    def transport(self, x, y):
        pass

    @abstractmethod
    def transport_center(self, dx, dy):
        pass

    @abstractmethod
    def in_bounds(self, x, y):
        pass

    @abstractmethod
    def set_central_coord(self):
        pass

    @abstractmethod
    def add_figure(self, figure):
        pass

    @abstractmethod
    def is_coord_on_figure(self, x, y):
        pass

    @abstractmethod
    def set_color(self, col):
        pass

    @abstractmethod
    def fill(self, col):
        pass

    @abstractmethod
    def set_thickness(self, th):
        pass

    @abstractmethod
    def draw_selected(self, painter):
        pass

    @abstractmethod
    def draw(self, painter, col, th, x, y):
        pass

    @abstractmethod
    def select(self):
        pass

    @abstractmethod
    def deselect(self):
        pass

    @abstractmethod
    def set_end_coord(self, x2, y2):
        pass

    @abstractmethod
    def set_start_coord(self, x1, y2):
        pass
