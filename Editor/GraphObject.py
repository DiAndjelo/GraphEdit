from copy import deepcopy
from math import sqrt

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QLinearGradient
from PyQt5.QtWidgets import QMainWindow, QComboBox, QWidget, QColorDialog, \
    QDialog, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QSpinBox

from Editor.Painter import Painter
from Figures.Circle import Circle
from Figures.Combiner import Combiner
from Figures.Hand import Hand
from Figures.Line import Line
from Figures.Group import Group
from Figures.Rectangle import Rectangle
from Forms.FillForm import FillForm
from Forms.SettingsInEditorForm import SettingsInEditorForm


class GraphObject(QMainWindow):
    """
    Инициализация класса GraphObject
    """
    def __init__(self, width=640, height=480, color=QColor('white'), file_name='', objects=None):
        super().__init__()
        # Инициализация обьектов
        if objects is None:
            objects = []
        self.objects = objects
        # Собираем параметры с инициализируещей формы
        self.file_name = file_name
        self.height = height
        self.width = width
        self.color = color
        # Переменные, отвечающие за историю операций
        self.temp = []
        self.history = [[]]
        self.history_flag = False
        self.state_number = 0
        # Был ли клик
        self.click = False
        # Текущий инструмент
        self.instrument = None
        # Текущий объект
        self.cur_object = None
        # Установка фокуса как при табуляции, так и при нажатии
        self.setFocusPolicy(Qt.StrongFocus)
        # Включаем поддержку отслеживания действий мышью
        self.setMouseTracking(True)
        # Флаг изменения параметров
        self.edit_fl = False
        # Флаг передвижения
        self.is_moving = False
        # Инициализация кнопочек
        self.make_forms()
        # ToDo: Параметры мыши?
        self.gr_x1 = None
        self.gr_x2 = None
        self.gr_y1 = None
        self.gr_y2 = None
        # Начальный цвет ручки
        self.line_color = QColor('black')
        self.fill_color = None

    # ============================================= GraphObject Events ============================================= #

    def instrumentChanged(self):
        """
        Изменение используемого инструмента
        """
        # Дергаем выбранный инструмент
        self.get_instrument()
        # Убираем фокус с каждого обьекта
        for o in self.objects:
            if o.selected:
                o.deselect()
        # Очищаем флаги движения клика и выбранного объекта
        self.is_moving = False
        self.click = False
        self.cur_object = None
        self.update()

    def paintEvent(self, e):
        """
        Событие отрисовки
        """
        self.draw_current_image()
        self.store_current_state()

    def keyPressEvent(self, event):
        """
        По нажатию стрелок влево-вправо манипулирем историей операций
        """
        key = event.key()
        if key == Qt.Key_Right:
            if self.state_number + 1 < len(self.history):
                self.state_number += 1
                self.objects = deepcopy(self.history[self.state_number])
                self.update()

        if key == Qt.Key_Left:
            if self.state_number - 1 >= 0:
                self.was_back = True
                self.state_number -= 1
                self.objects = deepcopy(self.history[self.state_number])
                self.update()

    def spinboxChanged(self, value):
        """
        Если измененно значение толщины со спинбокса - вызываем change_thick
        """
        self.change_thick(value)

    def mousePressEvent(self, event):
        """
        Действия по клику на мышь
        """
        # Дергаем координаты события
        x, y = event.pos().x(), event.pos().y()
        # Если действие находится не в пределах области рисования - дропаем событие
        if not self.in_bounds(x, y):
            return
        # Если нет флага edit_fl - дёргаем выбранный инструмент
        if not self.edit_fl:
            self.get_instrument()
        # Дергаем толщину контура
        self.get_line_thick()
        # Действия по выбранному инструменту
        if self.instrument != "Select":
            # Если нажали в пустое место - убираем все флаги
            if self.click and self.is_moving and self.cur_object is not None:
                self.edit_ok()
                self.click = False
                return
            # Увеличиваем размер истории на 1
            self.history = self.history[:self.state_number + 1]
            self.history_flag = True
            # При клике куда либо
            if self.click:
                self.click = False
                if self.in_bounds(x, y):
                    # Если клик находится в области рисования
                    if self.instrument == 'Circle' and self.cur_object is not None:
                        # Дествия для выбранного круга
                        if self.circle_in_bounds(x, y):
                            if self.cur_object is not None:
                                if self.is_moving:
                                    # Изменение положения
                                    self.cur_object.move(x, y)
                                else:
                                    # Установка положения
                                    self.cur_object.set_end_coord(x, y)
                    else:
                        # Действия для остальных обьектов
                        if self.cur_object is not None:
                            if self.is_moving:
                                # Изменение положения
                                self.cur_object.move(x, y)
                            else:
                                # Установка положения
                                self.cur_object.set_end_coord(x, y)
                    if not self.edit_fl:
                        # Если не установлен флаг редактирования обьекта - добавляем обьект по клику
                        self.objects.append(self.cur_object)
                    # Устанавливаем обьекту цвет и ширину(на случай создания нового объекта)
                    self.cur_object.set_color(self.line_color)
                    self.cur_object.set_thickness(self.get_line_thick())
                    if self.edit_fl:
                        # Снимаем все флаги по завершению редактирования
                        self.edit_ok()
            else:
                if self.in_bounds(x, y):
                    # Создание обьектов, при нажатии на пустое место с выбранным инструментом
                    self.click = True
                    if self.instrument == "Line":
                        self.cur_object = Line(x, y)
                    elif self.instrument == "Hand":
                        self.cur_object = Hand(x, y)
                    elif self.instrument == 'Rectangle':
                        self.cur_object = Rectangle(x, y)
                    elif self.instrument == 'Circle':
                        self.cur_object = Circle(x, y)
        else:
            # Действия по select
            self.history_flag = False
            for obj in self.objects:
                # Двигаем или снимаем фокус с выбраных обьектов
                if obj.is_coord_on_figure(x, y):
                    if obj.selected:
                        obj.move_or_deselect(x, y)
                        if obj.selected:
                            self.is_moving = True
                            self.edit()
                    else:
                        obj.select()
                        self.is_moving = True
        self.update()

    def mouseMoveEvent(self, event):
        """
        Действия по зажатой клавише мыши
        """
        # Дергаем координаты события
        x, y = event.pos().x(), event.pos().y()

        if self.cur_object is not None and self.click:
            # Двигаем обьекты
            if self.in_bounds(x, y):
                if self.instrument == 'Circle' and self.cur_object is not None:
                    if self.circle_in_bounds(x, y):
                        if self.is_moving:
                            self.cur_object.move(x, y)
                        else:
                            self.cur_object.set_end_coord(x, y)
                else:
                    if self.is_moving:
                        self.cur_object.move(x, y)
                    else:
                        self.cur_object.set_end_coord(x, y)

            self.temp.append(self.cur_object)

        self.update()

    # =================================================== Views ==================================================== #

    def make_forms(self):
        """
        Создание кнопочек
        """
        # Комбобокс с инструментами
        self.instruments_lbl = QLabel('Instruments', self)
        self.instruments_lbl.move(10, 20)
        self.instruments_lbl.resize(100, 35)
        self.instruments = QComboBox(self)
        self.instruments.addItems(["Line", "Hand", "Rectangle", "Circle", "Select"])
        self.instruments.move(10, 50)
        self.instruments.resize(100, 35)
        self.instruments.currentIndexChanged.connect(self.instrumentChanged)
        # Кнопка изменения цвета
        self.color_button = QPushButton('Color', self)
        self.color_button.move(120, 50)
        self.color_button.resize(100, 35)
        self.color_button.clicked.connect(self.color_picker)
        self.color_lbl = QLabel('Color', self)
        self.color_lbl.move(230, 20)
        self.color_lbl.resize(100, 35)
        # Кнопка изменения ширины
        self.thick_button = QSpinBox(self)
        self.thick_button.move(340, 50)
        self.thick_button.resize(100, 35)
        self.thick_button.setMinimum(2)
        self.thick_button.setMaximum(60)
        self.thick_button.valueChanged.connect(self.spinboxChanged)
        # Лейбл с показом текущей ширины
        self.thick_lbl = QLabel('Thickness', self)
        self.thick_lbl.move(340, 20)
        self.thick_lbl.resize(100, 35)
        # Как я понял - кнопка комбинирования обьектов
        self.combine_button = QPushButton('Combine', self)
        self.combine_button.move(780, 50)
        self.combine_button.resize(100, 35)
        self.combine_button.clicked.connect(self.combine)
        self.combine_button.hide()
        # Кнопка удаления обьекта
        self.delete_button = QPushButton('Delete', self)
        self.delete_button.move(670, 50)
        self.delete_button.resize(100, 35)
        self.delete_button.clicked.connect(self.delete)
        self.delete_button.hide()
        # Кнопка изменения цвета
        self.change_color_button = QPushButton('Color', self)
        self.change_color_button.move(120, 50)
        self.change_color_button.resize(100, 35)
        self.change_color_button.clicked.connect(self.change_color)
        self.change_color_button.hide()
        # Кнопка изменения бэкграунда(вызывается первоначальная форма)
        self.background_button = QPushButton('BackColor', self)
        self.background_button.move(450, 50)
        self.background_button.resize(100, 35)
        self.background_button.clicked.connect(self.set_settings)
        # Заполнение фигуры(возможность заполнения градиентом из 2х цветов)
        self.fill_button = QPushButton('Fill', self)
        self.fill_button.move(560, 50)
        self.fill_button.resize(100, 35)
        self.fill_button.clicked.connect(self.fill)
        self.fill_button.hide()
        # Кнопка сохранение всей красоты
        self.save_button = QPushButton('Save', self)
        self.save_button.move(890, 50)
        self.save_button.resize(100, 35)
        self.save_button.clicked.connect(self.save)
        self.save_button.show()
        # Кнопки для изменения типа градиента
        self.grad_instruments = QComboBox(self)
        self.grad_instruments.addItems(["Linear", "Radial"])
        self.grad_instruments.move(10, 50)
        self.grad_instruments.resize(1300, 70)
        self.grad_instruments.hide()

    def set_instrument(self, o):
        """
        Применить инструмент
        """
        # ... если cur.object объект класса Circle ...
        if isinstance(o, Circle):
            self.instrument = 'Circle'
        elif isinstance(o, Rectangle):
            self.instrument = 'Rectangle'
        elif isinstance(o, Line):
            self.instrument = 'Line'
        elif isinstance(o, Hand):
            self.instrument = 'Hand'
        elif isinstance(o, Group):
            self.instrument = 'Object'

    def get_instrument(self):
        """
        Дергает выбранный инструмент и применяет флаги show hide в зависимости от выбранного инструмента
        """
        self.instrument = self.instruments.currentText()
        if self.instrument == "Select":

            self.instruments.show()
            self.thick_button.show()
            self.change_color_button.show()
            self.combine_button.show()
            self.delete_button.show()
            self.fill_button.show()
            self.color_button.hide()

        elif self.instrument == 'Line' \
                or self.instrument == "Hand" \
                or self.instrument == "Rectangle" \
                or self.instrument == "Circle":
            self.combine_button.hide()

            self.change_color_button.hide()
            self.combine_button.hide()
            self.delete_button.hide()
            self.fill_button.hide()

            self.instruments.show()
            self.thick_button.show()
            self.color_button.show()
        self.update()

    def edit(self):
        """
        Редактирование обьекта
        """
        # Выбор текущего обьекта
        for i in self.objects:
            if i.selected:
                self.cur_object = i
                break
        # Применение флагов и выбор инструмента, которым создан обьект
        if self.cur_object is not None:
            self.edit_fl = True
            self.click = True
            self.set_instrument(self.cur_object)

    def edit_ok(self):
        """
        Снятие флагов, фокуса, остановка движения обьекта
        """
        self.edit_fl = False
        self.cur_object.deselect()
        self.cur_object.stop_moving()
        self.instrument = 'Select'
        self.cur_object = None
        self.click = False
        self.is_moving = False

    def store_current_state(self):
        """
        Уведичиваем текущую историю
        """
        if self.history_flag and not self.click:
            self.history.append(deepcopy(self.objects))
            self.history_flag = False
            self.state_number += 1

    def set_settings(self):
        """
        Форма настройки редактора по клику на Background
        """
        form = SettingsInEditorForm(self)
        form.setFocus()

        vbox = QVBoxLayout()
        vbox.addWidget(form)
        self.setLayout(vbox)

        form.setGeometry(600, 200, 250, 500)
        form.show()

    def fill(self):
        """
        Заполнение выбранных обьектов выбранным цветов
        """
        form = FillForm(self)
        form.setFocus()

        vbox = QVBoxLayout()
        vbox.addWidget(form)
        self.setLayout(vbox)

        form.setGeometry(500, 500, 500, 800)
        form.show()
        form.exec()

        for e in self.objects:
            if e.selected:
                e.fill(self.fill_color)
        self.history_flag = True
        self.fill_color = None
        self.update()

    def get_line_thick(self):
        """
        Дергает толщину обьекта из кнопки толщины обьекта
        """
        thick = int(self.thick_button.text())
        return thick

    def get_line_color(self):
        return self.line_color

    def get_fill_color(self):
        return self.fill_color

    def color_picker(self):
        """
        Применяет выбранный цвет
        """
        self.line_color = QColorDialog.getColor()

    def change_color(self):
        """
        Изменение цвета выбранных обьектов
        """
        self.color_picker()
        for e in self.objects:
            if e.selected:
                e.deselect()
                e.set_color(self.line_color)
        self.history_flag = True
        self.update()

    def change_thick(self, th):
        """
        Изменение толщины выбранных обьектов
        """
        for e in self.objects:
            if e.selected:
                e.set_thickness(th)
        self.history_flag = True
        self.update()

    def save(self):
        """
        Сохранение всей красоты в svg
        """
        from Editor.SVGParser import SVGParser

        SVGParser(self.file_name).save2svg(self)

    def combine(self):
        """
        Собираем обьекты в кучу
        """
        li = []
        o = []
        obj = None
        for e in self.objects:
            if e.selected:
                e.deselect()
                if e is Group and obj is not None:
                    obj = e
                else:
                    li.append(e)
            else:
                o.append(e)
        self.history_flag = True
        o.append(Combiner.combine(li, obj))
        self.objects = o
        self.update()

    def delete(self):
        """
        Удаление обьекта
        """
        o = []
        for e in self.objects:
            if not e.selected:
                o.append(e)
        self.history_flag = True
        self.objects = o
        self.update()

    def draw_current_image(self):
        """
        Рисует текущее изобрашение
        """
        painter = Painter(self)

        painter.fillRect(230, 50, 100, 35, self.line_color)
        painter.fillRect(40, 150, self.width, self.height, self.color)

        for e in self.objects:
            if e is not None:
                e.draw(painter, None, None, self.get_max_x(), self.get_max_y())
            else:
                self.objects.remove(e)
        for e in self.temp:
            if e is not None:
                e.draw(painter, self.line_color, self.get_line_thick(), None, None)
        self.temp = []

    # ================================================== Checkers ================================================== #

    def in_bounds(self, x, y):
        """
        Возвращает по выбранным координатам находится ли обьект в пределах области рисования
        """
        if self.is_moving and (
                self.cur_object is not None) and (
                not self.cur_object.in_bounds(self.width, self.height)):
            self.edit_ok()
            return False

        return 40 <= x + self.get_line_thick() / 2 <= self.width + 40 and (
                150 <= y + self.get_line_thick() / 2 <= 150 + self.height) and (
                       40 <= x - self.get_line_thick() / 2 <= self.width + 40) and (
                       150 <= y - self.get_line_thick() / 2 <= 150 + self.height)

    def circle_in_bounds(self, x2, y2):
        # Находится ли круг в области рисования
        if self.is_moving and not self.cur_object.in_bounds(self.width, self.height):
            return False
        xr = self.cur_object.x1
        yr = self.cur_object.y1
        x = x2 - xr
        y = y2 - yr
        rad = sqrt(x * x + y * y)
        return self.in_bounds(xr + rad, yr) and (
            self.in_bounds(xr - rad, yr)) and (
                   self.in_bounds(xr, yr + rad)) and (
                   self.in_bounds(xr, yr - rad))

    def get_max_x(self):
        """
        Дергаем максимальное значение ширины области рисования
        """
        return 40 + self.width

    def get_max_y(self):
        """
        Дергаем максимальное значение высоты области рисования
        """
        return 150 + self.height
