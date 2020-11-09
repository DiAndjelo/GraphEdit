from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPen, QColor

from Figures.Figure import Figure


class Object(Figure):
    """
    Класс объекта, который отвечает за combined обьекты
    """
    def __init__(self, figures=None):
        super().__init__()
        if figures is None:
            figures = list()
        self.figures = figures
        self.selected = False

        self.center_x = None
        self.center_y = None

        self.center = False

    def stop_moving(self):
        self.center = False

    def move_or_deselect(self, x, y):
        if self.center_x - 10 <= x <= self.center_x + 10 \
                and self.center_y - 10 <= y <= self.center_y + 10\
                or self.center:
            self.center = True
            self.move(x, y)
        else:
            self.deselect()

    def move(self, x, y):
        if self.center_x - 10 <= x <= self.center_x + 10 \
                and self.center_y - 10 <= y <= self.center_y + 10\
                or self.center:
            self.transport(x, y)

    def transport(self, x, y):
        dx = x - self.center_x
        dy = y - self.center_y
        self.transport_center(dx, dy)

    def transport_center(self, dx, dy):
        self.center_y += dy
        self.center_x += dx
        for figure in self.figures:
            figure.transport_center(dx, dy)

    def in_bounds(self, x, y):
        for f in self.figures:
            if not f.in_bounds(x, y):
                return False
        return True

    def set_central_coord(self):
        x_min = None
        y_min = None
        y_max = None
        x_max = None

        for f in self.figures:
            if x_min is None or x_min > f.x1:
                x_min = f.x1
            elif x_max is None or x_max < f.x1:
                x_max = f.x1

            if x_min is None or x_min > f.x2:
                x_min = f.x2
            elif x_max is None or x_max < f.x2:
                x_max = f.x2

            if y_min is None or y_min > f.y1:
                y_min = f.y1
            elif y_max is None or y_max < f.y1:
                y_max = f.y1

            if y_min is None or y_min > f.y2:
                y_min = f.y2
            elif y_max is None or y_max < f.y2:
                y_max = f.y2

        self.center_x = (x_max + x_min) / 2
        self.center_y = (y_max + y_min) / 2

    def add_figure(self, figure):
        if figure is Object:
            for e in figure.figures:
                self.figures.append(e)
        else:
            self.figures.append(figure)

    def is_coord_on_figure(self, x, y):
        self.set_central_coord()
        if self.center_x - 10 <= x <= self.center_x + 10 \
                and self.center_y - 10 <= y <= self.center_y + 10 or self.center:
            return True
        for e in self.figures:
            if e.is_coord_on_figure(x, y):
                return True

    def set_color(self, col):
        for e in self.figures:
            e.set_color(col)

    def fill(self, col):
        for e in self.figures:
            e.fill(col)

    def set_thickness(self, th):
        for e in self.figures:
            e.set_thickness(th)

    def draw_selected(self, painter):
        self.set_central_coord()
        pen = QPen(QColor('black'), 2, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawEllipse(QPoint(self.center_x, self.center_y), 10, 10)

    def draw(self, painter, col, th, x, y):

        if self.selected:
            self.draw_selected(painter)

        for e in self.figures:
            sel = e.selected
            e.selected = False
            e.draw(painter, col, th, x, y)
            e.selected = sel

    def select(self):
        self.selected = True
        for e in self.figures:
            e.select()

    def deselect(self):
        self.selected = False
        for e in self.figures:
            e.deselect()

    def set_start_coord(self, x1, y2):
        pass

    def set_end_coord(self, x2, y2):
        pass
