from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QColorDialog, QPushButton, QSpinBox, QLabel, QWidget


class SettingsInEditorForm(QWidget):
    """
    Форма изменения параметров редактора
    """
    def __init__(self, graph_object=None):
        super().__init__()

        self.graph_object = graph_object

        self.resize(100, 100)

        self.lbl_height = QLabel("Enter height", self)
        self.lbl_height.move(20, 20)
        self.lbl_height.resize(200, 50)
        self.height_box = QSpinBox(self)
        self.height_box.move(20, 70)
        self.height_box.resize(200, 70)
        self.height_box.setMinimum(200)
        self.height_box.setMaximum(1300)
        self.height_box.setValue(graph_object.height)

        self.lbl_width = QLabel("Enter width", self)
        self.lbl_width.move(20, 140)
        self.lbl_width.resize(200, 70)
        self.width_box = QSpinBox(self)
        self.width_box.move(20, 190)
        self.width_box.resize(200, 70)
        self.width_box.setMinimum(200)
        self.width_box.setMaximum(3000)
        self.width_box.setValue(graph_object.width)

        self.button = QPushButton('COLOR', self)
        self.button.move(20, 300)
        self.button.resize(200, 70)
        self.button.clicked.connect(self.color_picker)

        self.button = QPushButton('OK', self)
        self.button.move(20, 400)
        self.button.resize(200, 70)
        self.button.clicked.connect(self.on_click)

        self.color = graph_object.color

    def color_picker(self):
        self.color = QColorDialog.getColor()
        self.update()

    def on_click(self):
        self.graph_object.width = int(self.width_box.text())
        self.graph_object.height = int(self.height_box.text())
        self.graph_object.color = self.color
        self.close()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.fillRect(240, 300, 200, 70, self.color)
