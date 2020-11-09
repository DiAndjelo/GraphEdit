from PyQt5.QtGui import QPainter

from Editor.Properties import PropertiesGroup


class Painter(QPainter):
    """
    Инициализация класса Painter - графического редактора
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.properties = PropertiesGroup(line_color=self.parent.get_line_color(),
                                          line_thick=self.parent.get_line_thick(),
                                          fill_color=self.parent.get_fill_color())

