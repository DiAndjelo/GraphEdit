import math
from math import sqrt

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPen, QColor, QBrush
from Figures.Figure import Figure


class Circle(Figure):
    """
    Класс объекта круг
    """
    def __init__(self, x1, y1, color=None, th=None):
        super().__init__()
        self.x1 = x1
        self.y1 = y1
        self.color = color
        self.thick = th
        self.x2 = x1
        self.y2 = y1
        self.selected = False
        self.fill_color = None
        self.unlighter = self.color
        self.center_x = x1
        self.center_y = y1

        self.center = False
        self.second = False

        self.rad = None

    # ================================================== Movement ================================================== #

    def move(self, x, y):
        if self.x1 - 10 <= x <= self.x1 + 10 \
                and self.y1 - 10 <= y <= self.y1 + 10 or self.center:
            self.center = True
            self.transport_center(x - self.x1, y - self.y1)
        elif self.x1 - 10 <= x - self.rad <= self.x1 + 10 \
                and self.y1 - 10 <= y <= self.y1 + 10 or self.second:
            self.second = True
            self.set_end_coord(x, y)

    def stop_moving(self):
        self.center = False
        self.second = False

    def move_or_deselect(self, x, y):
        if self.center_x - 10 <= x <= self.center_x + 10 \
                and self.center_y - 10 <= y <= self.center_y + 10 or self.center\
                or self.center_x - 10 <= x - self.rad <= self.center_x + 10 \
                and self.center_y - 10 <= y <= self.center_y + 10 or self.second:
            self.move(x, y)
        else:
            self.deselect()

    def transport(self, x, y):
        pass

    def transport_center(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        try:
            if self.fill_color.col2 is not None:
                self.fill_color.x1 += dx
                self.fill_color.x2 += dx

                self.fill_color.y1 += dy
                self.fill_color.y2 += dy
        except AttributeError:
            pass
        self.center_y = self.y1
        self.center_x = self.x1

    # ============================================ Checkers and setters ============================================ #

    def in_bounds(self, x, y):
        return 40 <= self.x1 + self.rad <= x + 40 and \
               150 <= self.y1 + self.rad <= 150 + y and \
               40 <= self.x1 - self.rad <= x + 40 \
               and 150 <= self.y1 - self.rad <= 150 + y

    def is_coord_on_figure(self, x, y):

        if self.selected and (self.center_x - 10 <= x <= self.center_x + 10
                              and self.center_y - 10 <= y <= self.center_y + 10 or self.center
                              or self.center_x - 10 <= x - self.rad <= self.center_x + 10
                              and self.center_y - 10 <= y <= self.center_y + 10 or self.second):
            return True

        if self.fill_color is not None:
            return (y - self.y1) ** 2 + (x - self.x1) ** 2 <= self.rad ** 2

        th = self.thick / 2
        return (self.rad + th) ** 2 >= (y - self.y1) ** 2 + (x - self.x1) ** 2 >= (self.rad - th) ** 2

    def set_central_coord(self):
        pass

    def set_start_coord(self, x, y):
        self.x1 = x
        self.y1 = y

        self.center_y = self.y1
        self.center_x = self.x1

    def set_end_coord(self, x2, y2):
        self.x2 = x2
        self.y2 = y2
        x = self.x1 - self.x2
        y = self.y1 - self.y2
        self.rad = sqrt(x * x + y * y)

    def set_thickness(self, th):
        self.thick = th

    def set_color(self, col):
        self.color = col

    # =================================================== Actions ================================================== #

    def select(self):
        self.selected = True
        self.unlighter = self.color
        self.color = QColor('red')

    def deselect(self):
        self.selected = False
        self.color = self.unlighter

    def add_figure(self, figure):
        pass

    def fill(self, col):
        self.fill_color = col

        if self.fill_color.col2 is not None:
            self.fill_color.x1 += self.x1 - self.rad
            self.fill_color.x2 += self.x1 - self.rad

            self.fill_color.y1 += self.y1 - self.rad
            self.fill_color.y2 += self.y1 - self.rad

    def draw_selected(self, painter):
        pass

    def draw(self, painter, col, th, x, y):

        if col is None:
            col = self.color
        if th is None:
            th = self.thick
        pen = QPen(col, th, Qt.SolidLine)
        painter.setPen(pen)

        changed = False
        if y is not None:
            if self.y1 - self.rad > y:
                return

            if self.rad + self.y1 > y:
                a = math.acos((y - self.y1) / self.rad) * 180 / math.pi

                s = -(90 - a)
                start = s * 16

                e = (90 - a) * 2 + 180
                span = e * 16

                changed = True

        if x is not None:
            if self.x1 - self.rad > x:
                return

            if self.rad + self.x1 > x:
                a = math.acos((x - self.x1) / self.rad) * 180 / math.pi

                if not changed:
                    s = a
                    start = s * 16
                    e = (90 - a) * 2 + 180
                    span = e * 16
                else:
                    s = a
                    start1 = s * 16
                    e = (90 - a) * 2 + 180
                    span1 = e * 16

                    res_s = max(start, start1)
                    end = min(start + span, start1 + span1)
                    span = end - res_s
                    start = res_s
                changed = True

        if self.fill_color is not None:
            col = self.fill_color.get_color()
            brush = QBrush(col)
            painter.setBrush(brush)

        else:
            brush = QBrush(QColor(255, 255, 255, alpha=0))
            painter.setBrush(brush)

        if changed:
            painter.drawArc(self.x1 - self.rad, self.y1 - self.rad,
                            self.rad * 2, self.rad * 2,
                            start, span)
        else:
            painter.drawEllipse(QPoint(self.x1, self.y1), self.rad, self.rad)

        if self.selected:
            pen = QPen(QColor('black'), 2, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawEllipse(QPoint(self.center_x, self.center_y), 10, 10)
            painter.drawEllipse(QPoint(self.center_x + self.rad, self.center_y), 10, 10)
