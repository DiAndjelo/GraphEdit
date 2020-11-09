from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPen, QColor
from Figures.Figure import Figure
from Figures.Line import Line


class Rectangle(Figure):
    """
    Класс объекта прямоугольник
    """
    def __init__(self, x1, y1, color=None, th=None):
        super().__init__()
        self.x1 = x1
        self.y1 = y1

        self.x2 = x1
        self.y2 = y1

        self.color = color
        self.thick = th
        self.selected = False

        self.fill_color = None

        self.center = False
        self.first = False
        self.second = False

    # ================================================== Movement ================================================== #

    def move(self, x: int, y: int) -> None:
        if self.center_x - 10 <= x <= self.center_x + 10 \
                and self.center_y - 10 <= y <= self.center_y + 10\
                or self.center:
            self.center = True
            self.transport(x, y)
        elif self.x1 - 10 <= x <= self.x1 + 10 \
                and self.y1 - 10 <= y <= self.y1 + 10\
                or self.first:
            self.first = True
            self.set_start_coord(x, y)
        elif self.x2 - 10 <= x <= self.x2 + 10 \
                and self.y2 - 10 <= y <= self.y2 + 10\
                or self.second:
            self.second = True
            self.set_end_coord(x, y)

    def stop_moving(self) -> None:
        self.center = False
        self.first = False
        self.second = False

    def move_or_deselect(self, x: int, y: int) -> None:
        if self.center_x - 10 <= x <= self.center_x + 10 \
                and self.center_y - 10 <= y <= self.center_y + 10 or self.center\
                or self.x1 - 10 <= x <= self.x1 + 10 \
                and self.y1 - 10 <= y <= self.y1 + 10 or self.first\
                or self.x2 - 10 <= x <= self.x2 + 10 \
                and self.y2 - 10 <= y <= self.y2 + 10 or self.second:
            self.move(x, y)
        else:
            self.deselect()

    def transport(self, x: int, y: int) -> None:
        dx = x - self.center_x
        dy = y - self.center_y
        self.transport_center(dx, dy)

    def transport_center(self, dx: int, dy: int) -> None:
        for i in self.lines:
            i.transport_center(dx, dy)

        self.x1 += dx
        self.y1 += dy

        self.x2 += dx
        self.y2 += dy

        try:
            if self.fill_color.col2 is not None:
                self.fill_color.x1 += dx
                self.fill_color.x2 += dx

                self.fill_color.y1 += dy
                self.fill_color.y2 += dy
        except AttributeError:
            pass

    # ============================================ Checkers and setters ============================================ #

    def in_bounds(self, x, y):
        for i in self.lines:
            if not i.in_bounds(x, y):
                return False
        return True

    def is_coord_on_figure(self, x, y):

        if self.fill_color is not None:
            if self.x1 < self.x2:
                minx = self.x1
                miny = self.y1

                maxx = self.x2
                maxy = self.y2
            else:
                minx = self.x2
                miny = self.y2

                maxx = self.x1
                maxy = self.y1
            return minx <= x <= maxx and miny <= y <= maxy

        self.set_central_coord()
        if self.selected and (self.center_x - 10 <= x <= self.center_x + 10 and
                              self.center_y - 10 <= y <= self.center_y + 10 or
                              self.center):
            return True

        for line in self.lines:
            if line.is_coord_on_figure(x, y):
                return True

    def set_central_coord(self):
        self.center_x = (self.x1 + self.x2) / 2
        self.center_y = (self.y1 + self.y2) / 2

    def set_start_coord(self, x1, y1):

        self.x1 = x1
        self.y1 = y1
        self.lines = []
        self.lines.append(Line(self.x1, self.y1, self.x1, self.y2))
        self.lines.append(Line(self.x1, self.y1, self.x2, self.y1))
        self.lines.append(Line(self.x2, self.y2, self.x1, self.y2))
        self.lines.append(Line(self.x2, self.y2, self.x2, self.y1))

    def set_end_coord(self, x2, y2):

        self.x2 = x2
        self.y2 = y2

        self.lines = []
        self.lines.append(Line(self.x1, self.y1, self.x1, y2))
        self.lines.append(Line(self.x1, self.y1, x2, self.y1))
        self.lines.append(Line(x2, y2, self.x1, y2))
        self.lines.append(Line(x2, y2, x2, self.y1))

    def set_thickness(self, thickness):
        self.thick = thickness
        for line in self.lines:
            line.set_thickness(self.thick)

    def set_color(self, col):
        self.color = col
        for line in self.lines:
            line.color = col

    # =================================================== Actions ================================================== #

    def select(self):
        self.selected = True
        for line in self.lines:
            line.select()

    def deselect(self):
        self.selected = False
        for line in self.lines:
            line.deselect()

    def add_figure(self, figure):
        pass

    def fill(self, color):
        self.fill_color = color
        if self.fill_color.col2 is not None:
            self.fill_color.x1 += self.x1
            self.fill_color.x2 += self.x1

            self.fill_color.y1 += self.y1
            self.fill_color.y2 += self.y1

    def draw_selected(self, painter):
        pass

    def draw(self, painter, color, thickness, x, y):

        if self.color is not None:
            color = self.color
        if self.thick is not None:
            thickness = self.thick

        for line in self.lines:
            sel = line.selected
            line.selected = False
            line.draw(painter, color, thickness, x, y)
            line.selected = sel

        if self.fill_color is not None:

            minx = min(self.x1, self.x2)
            miny = min(self.y1, self.y2)
            color = self.fill_color.get_color()

            painter.fillRect(minx + self.thick / 2,
                             miny + self.thick / 2,
                             abs(self.x1 - self.x2) - self.thick,
                             abs(self.y1 - self.y2) - self.thick,
                             color)

        if self.selected:
            self.set_central_coord()
            pen = QPen(QColor('black'), 2, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawEllipse(QPoint(self.center_x, self.center_y), 10, 10)
            painter.drawEllipse(QPoint(self.x1, self.y1), 10, 10)
            painter.drawEllipse(QPoint(self.x2, self.y2), 10, 10)
