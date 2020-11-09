from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPen, QColor
from Figures.Figure import Figure
from Figures.Line import Line


class Hand(Figure):

    def __init__(self, x1, y1, color=None, th=None):
        super().__init__()
        self.x1 = x1
        self.y1 = y1
        self.lines = []
        self.color = color
        self.thick = th
        self.selected = False

        self.center_x = None
        self.center_y = None

        self.x2 = x1
        self.y2 = y1

        self.center = False

    def in_bounds(self, x, y):
        for i in self.lines:
            if not i.in_bounds(x, y):
                return False
        return True

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
        for line in self.lines:
            line.transport_center(dx, dy)

        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def set_central_coord(self):
        x_min = None
        y_min = None
        y_max = None
        x_max = None

        for f in self.lines:
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

    def set_end_coord(self, x2, y2):
        self.lines.append(Line(self.x1, self.y1, x2, y2))
        self.x1 = x2
        self.y1 = y2

    def set_color(self, col):
        self.color = col
        for line in self.lines:
            line.color = col

    def set_thickness(self, th):
        self.thick = th
        for line in self.lines:
            line.set_thickness(self.thick)

    def draw(self, painter, col, th, x, y):
        if self.color is not None:
            col = self.color
        if self.thick is not None:
            th = self.thick
        for line in self.lines:
            sel = line.selected
            line.selected = False
            line.draw(painter, col, th, x, y)
            line.selected = sel

        if self.selected:
            self.set_central_coord()
            pen = QPen(QColor('black'), 2, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawEllipse(QPoint(self.center_x, self.center_y), 10, 10)

    def is_coord_on_figure(self, x, y):
        self.set_central_coord()
        if self.selected \
                and (self.center_x - 10 <= x <= self.center_x + 10
                     and self.center_y - 10 <= y <= self.center_y + 10
                     or self.center):
            return True
        for line in self.lines:
            if line.is_coord_on_figure(x, y):
                return True

    def select(self):
        self.selected = True
        for line in self.lines:
            line.select()

    def deselect(self):
        self.selected = False
        for line in self.lines:
            line.deselect()

    def fill(self, c):
        pass

    def draw_selected(self, painter):
        pass

    def set_start_coord(self, x1, y2):
        pass

    def add_figure(self, figure):
        pass
