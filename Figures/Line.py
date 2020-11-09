from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPen, QColor
from Figures.Figure import Figure


class Line(Figure):

    def __init__(self, x1, y1, x2=None, y2=None, color=None, th=None):
        super().__init__()
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        self.center_x = None
        self.center_y = None

        self.color = color
        self.thick = th
        self.selected = False
        self.unlighter = color

        self.center = False
        self.first = False
        self.second = False

    def stop_moving(self):
        self.center = False
        self.first = False
        self.second = False

    def in_bounds(self, w, h):

        if self.x2 is None or self.y2 is None:
            return True
        if self.thick is None:
            th = 10
        else:
            th = self.thick
        return (40 <= self.x1 + th / 2 <= w + 40 and
                150 <= self.y1 + th / 2 <= 150 + h and
                40 <= self.x2 + th / 2 <= w + 40 and
                150 <= self.y2 + th / 2 <= 150 + h and
                40 <= self.x1 - th / 2 <= w + 40 and
                150 <= self.y1 - th / 2 <= h + 150 and
                40 <= self.x2 - th / 2 <= w + 40 and
                150 <= self.y2 - th / 2 <= h + 150)

    def transport(self, x, y):
        dx = x - self.center_x
        dy = y - self.center_y
        self.transport_center(dx, dy)

    def transport_center(self, dx, dy):
        self.x1 += dx
        self.x2 += dx

        self.y1 += dy
        self.y2 += dy

    def set_thickness(self, th):
        self.thick = th

    def set_color(self, col):
        self.color = col

    def set_end_coord(self, x2, y2):
        self.x2 = x2
        self.y2 = y2

    def set_start_coord(self, x1, y1):
        self.x1 = x1
        self.y1 = y1

    def move_or_deselect(self, x, y):
        if self.center_x - 10 <= x <= self.center_x + 10 \
                and self.center_y - 10 <= y <= self.center_y + 10 or self.center\
                or self.x1 - 10 <= x <= self.x1 + 10 \
                and self.y1 - 10 <= y <= self.y1 + 10 or self.first\
                or self.x2 - 10 <= x <= self.x2 + 10 \
                and self.y2 - 10 <= y <= self.y2 + 10 or self.second:
            self.move(x, y)
        else:
            self.deselect()

    def move(self, x, y):
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

    def set_central_coord(self):
        self.center_x = (self.x1 + self.x2) / 2
        self.center_y = (self.y1 + self.y2) / 2

    def draw(self, painter, col, th, x, y):

        dr_x1 = self.x1
        dr_x2 = self.x2
        dr_y1 = self.y1
        dr_y2 = self.y2

        if self.color is not None:
            col = self.color
        else:
            self.color = col
        if self.thick is not None:
            th = self.thick
        else:
            self.thick = th

        changed = False

        if x is not None:
            if self.x1 > x and self.x2 > x:
                return
            if self.x1 > x:
                dr_x1 = x
                dr_y1 = self.f(x, y)
                changed = True
            if self.x2 > x:
                dr_x2 = x
                dr_y2 = self.f(x, y)
                changed = True

        if y is not None:
            if self.y1 > y and self.y2 > y:
                return
            if self.y1 > y and not changed:
                dr_y1 = y
                dr_x1 = self.g(y, x)
            if self.y2 > y and not changed:
                dr_y2 = y
                dr_x2 = self.g(y, x)
        pen = QPen(col, th, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(dr_x1, dr_y1, dr_x2, dr_y2)

        if self.selected:
            self.draw_selected(painter)

    def draw_selected(self, painter):
        self.set_central_coord()
        pen = QPen(QColor('black'), 2, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawEllipse(QPoint(self.center_x, self.center_y), 10, 10)
        painter.drawEllipse(QPoint(self.x1, self.y1), 10, 10)
        painter.drawEllipse(QPoint(self.x2, self.y2), 10, 10)

    def get_y_shift(self):
        x = abs(self.x1 - self.x2)
        y = abs(self.y1 - self.y2)
        if y == 0 or x == 0:
            return 0
        else:
            tg_fi = x / y
        return tg_fi * x

    def f(self, x0, y0):
        if self.x1 == self.x2:
            return self.y1
        dx = (self.x2 - self.x1)
        dy = (self.y1 - self.y2)
        return ((self.x2 * self.y1 - self.x1 * self.y2) - dy * x0) / dx

    def g(self, y0, x0):
        if self.y1 == self.y2:
            return self.x1
        dx = (self.x2 - self.x1)
        dy = (self.y1 - self.y2)
        return ((self.x2 * self.y1 - self.x1 * self.y2) - dx * y0) / dy

    def is_coord_on_figure(self, x, y):

        self.set_central_coord()
        if self.selected and (self.center_x - 10 <= x <= self.center_x + 10
                              and self.center_y - 10 <= y <= self.center_y + 10 or self.center
                              or self.x1 - 10 <= x <= self.x1 + 10
                              and self.y1 - 10 <= y <= self.y1 + 10 or self.first
                              or self.x2 - 10 <= x <= self.x2 + 10
                              and self.y2 - 10 <= y <= self.y2 + 10 or self.second):
            return True

        absx = abs(self.x1 - self.x2)
        absy = abs(self.y1 - self.y2)
        th = self.thick / 2
        if absy < 0.00001:

            if self.x1 > self.x2:
                x1 = self.x2
                x2 = self.x1
            else:
                x1 = self.x1
                x2 = self.x2

            y1 = self.y1 - th
            y2 = self.y2 + th

            return x1 <= x <= x2 and y1 <= y <= y2

        if absx < 0.00001:

            if self.y1 > self.y2:
                y1 = self.y2
                y2 = self.y1
            else:
                y1 = self.y1
                y2 = self.y2

            x1 = self.x1 - th
            x2 = self.x2 + th

            return x1 <= x <= x2 and y1 <= y <= y2

        if self.x1 > self.x2:
            minx = self.x2
            maxx = self.x1
        else:
            minx = self.x1
            maxx = self.x2
        if self.y1 > self.y2:
            miny = self.y2
            maxy = self.y1
        else:
            miny = self.y1
            maxy = self.y2

        dy = self.get_y_shift()
        y1 = self.y1 + dy
        y2 = self.y2 + dy

        k = (y2 - y1) / (self.x2 - self.x1)

        return (maxx >= x >= minx and
                maxy >= y >= miny and
                k * x + (self.y1 - k * self.x1) + th > y > k * x + (self.y1 - k * self.x1) - th)

    def select(self):
        self.selected = True
        self.unlighter = self.color
        self.color = QColor('red')

    def deselect(self):
        self.selected = False
        self.color = self.unlighter

    def fill(self, c):
        pass

    def add_figure(self, figure):
        pass
