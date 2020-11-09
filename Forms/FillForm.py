from PyQt5.QtGui import QLinearGradient, QColor, QPainter
from PyQt5.QtWidgets import QColorDialog, QPushButton, QComboBox, QDialog


class FillForm(QDialog):
    """
    Форма заполнения фигуры цветом
    """
    def __init__(self, p):
        super().__init__()

        self.resize(400, 400)

        self.p = p

        self.first = None
        self.second = None
        self.click = False

        self.instruments = QComboBox(self)
        self.instruments.addItems(["Color", "Linear"])
        self.instruments.move(20, 300)
        self.instruments.resize(200, 70)
        self.instruments.currentIndexChanged.connect(self.instrumentChanged)

        self.button = QPushButton('OK', self)
        self.button.move(20, 400)
        self.button.resize(200, 70)
        self.button.clicked.connect(self.on_click)

        self.button0 = QPushButton('COLOR', self)
        self.button0.move(250, 50)
        self.button0.resize(200, 70)
        self.button0.clicked.connect(self.color1)

        self.button1 = QPushButton('COLOR 1', self)
        self.button1.move(250, 50)
        self.button1.resize(200, 70)
        self.button1.clicked.connect(self.color1)
        self.button1.hide()

        self.button2 = QPushButton('COLOR 2', self)
        self.button2.move(250, 130)
        self.button2.resize(200, 70)
        self.button2.clicked.connect(self.color2)
        self.button2.hide()

        self.instrument = 'Color'

        self.color = QColor('white')

        self.col1 = QColor('white')
        self.col2 = QColor('white')

    def instrumentChanged(self):
        self.instrument = self.instruments.currentText()
        if self.instrument == 'Color':
            self.button1.hide()
            self.button2.hide()
            self.button0.show()
        elif self.instrument == 'Linear':
            self.button1.show()
            self.button2.show()
            self.button0.hide()

    def color1(self):
        self.color_picker(True)

    def color2(self):
        self.color_picker(False)

    def color_picker(self, fl):
        if fl:
            self.col1 = QColorDialog.getColor()
        else:
            self.col2 = QColorDialog.getColor()
        self.update()

    def on_click(self):
        self.p.fill_color = self.color
        self.close()

    def paintEvent(self, e):
        painter = QPainter(self)

        if self.instrument == 'Color':
            if self.col1 is None:
                col = QColor('white')
            else:
                col = self.col1

            painter.fillRect(20, 50, 200, 200, col)

            self.color = FillFigure(self.col1)

        else:
            if self.col1 is None:
                col1 = QColor('white')
            else:
                col1 = self.col1
            if self.col2 is None:
                col2 = QColor('white')
            else:
                col2 = self.col2

            if self.first is None:
                self.first = [20, 50]
            if self.second is None:
                self.second = [21, 100]

            grad = QLinearGradient(self.first[0], self.first[1], self.second[0], self.second[1])
            grad.setColorAt(0, col1)
            grad.setColorAt(1, col2)
            painter.fillRect(20, 50, 200, 200, grad)

            self.color = FillFigure(self.col1, self.col2, self.first[0], self.first[1], self.second[0], self.second[1])

    def mousePressEvent(self, event):
        x, y = event.pos().x(), event.pos().y()

        if 20 <= x <= 220 and 50 <= y <= 250:

            if not self.click:
                self.click = True
                self.first = [x, y]

            else:
                self.click = False
                self.second = [x, y]
            self.update()


class FillFigure:
    """
    Заполнятор фигуры цветом
    """
    def __init__(self, c1, c2=None, x1=None, y1=None, x2=None, y2=None):

        self.col1 = c1
        self.col2 = c2

        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def get_color(self):
        if self.col2 is None:
            return self.col1
        else:
            grad = QLinearGradient(self.x1, self.y1, self.x2, self.y2)
            grad.setColorAt(0, self.col1)
            grad.setColorAt(1, self.col2)
            return grad
