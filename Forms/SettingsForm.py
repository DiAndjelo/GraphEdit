from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QSpinBox
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QMainWindow
from Editor.GraphObject import GraphObject


class SettingsForm(QMainWindow):
    """
    Форма для задания настроек редактора
    """
    def __init__(self):
        super().__init__()
        self.resize(100, 100)
        # Высота
        self.lbl_height = QLabel("Enter height", self)
        self.lbl_height.move(20, 20)
        self.lbl_height.resize(200, 50)
        self.height_box = QSpinBox(self)
        self.height_box.move(20, 70)
        self.height_box.resize(200, 70)
        self.height_box.setMinimum(200)
        self.height_box.setMaximum(1300)
        self.height_box.setValue(510)
        # Ширина
        self.lbl_width = QLabel("Enter width", self)
        self.lbl_width.move(20, 140)
        self.lbl_width.resize(200, 70)
        self.width_box = QSpinBox(self)
        self.width_box.move(20, 190)
        self.width_box.resize(200, 70)
        self.width_box.setMinimum(200)
        self.width_box.setMaximum(3000)
        self.width_box.setValue(920)
        # Цвет
        self.button = QPushButton('COLOR', self)
        self.button.move(20, 400)
        self.button.resize(200, 70)
        self.button.clicked.connect(self.color_picker)
        # Кнопка старта
        self.button = QPushButton('START', self)
        self.button.move(20, 500)
        self.button.resize(200, 70)
        self.button.clicked.connect(self.on_click)
        # Имя файла
        self.lbl_name = QLabel("Enter file's name", self)
        self.lbl_name.move(20, 250)
        self.lbl_name.resize(200, 70)
        self.name_box = QLineEdit(self)
        self.name_box.move(20, 300)
        self.name_box.resize(200, 70)

        self.color = QColor('white')

    def color_picker(self):
        """
        Изменение цвета и сохранение в self.color
        """
        self.color = QColorDialog.getColor()

    def on_click(self):
        """
        Нажатие кнопки START
        """
        self.close()
        # Закртытие первой формы и открытие окна редактора с передачей всех собранных параметров
        self.release_graph_object = ReleaseGraphObject(width=int(self.width_box.text()),
                                                       height=int(self.height_box.text()),
                                                       color=self.color,
                                                       file_name=self.name_box.text())
        self.setCentralWidget(self.release_graph_object)
        self.release_graph_object.setGeometry(100, 100, 1400, 700)
        self.release_graph_object.show()


class ReleaseGraphObject(QMainWindow):
    """
    Инициализация окна редактора Painter
    """
    def __init__(self, width, height, color, file_name):
        super().__init__()
        self.painter = GraphObject(width, height, color, file_name)
        self.painter.setGeometry(300, 100, 1000, 700)
        self.painter.show()

