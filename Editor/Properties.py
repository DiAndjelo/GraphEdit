from PyQt5.QtGui import QColor


class Properties:
    """
    Абстрактный класс свойств
    """
    def apply_props(self, painter):
        """
        Применение всех свойств к Painter'у
        :param painter: класс Painter
        """
        pass

    def get_list_prop(self):
        pass


class PropertiesGroup(Properties):
    """
    Класс свойств
    """
    def __init__(self, line_color=None, line_thick=None, fill_color=None):
        """
        Добавление свойств ручки и кисти
        """
        line_color = QColor(0, 0, 255, 155) if not line_color else line_color
        fill_color = QColor(0, 0, 255, 155) if not fill_color else fill_color
        line_thick = 1 if not line_thick else line_thick
        self.list_prop = dict(
            line_prop=LineProps(line_color, line_thick),
            fill_prop=FillProps(fill_color)
        )

    def apply_props(self, painter):
        self.list_prop.get('line_prop').apply_props(painter)
        self.list_prop.get('fill_prop').apply_props(painter)

    def get_list_prop(self):
        return self.list_prop


class LineProps(Properties):
    """
    Класс свойств ручки
    """
    def __init__(self, _line_color, _line_thick):
        self.line_color = _line_color
        self.line_thick = _line_thick

    def apply_props(self, painter):
        """
        Перезаписываем применение всех свойств к Painter'у для ручки
        :param painter: класс Painter
        """
        painter.line_color = self.line_color
        painter.line_thick = self.line_thick


class FillProps(Properties):
    """
    Класс свойств кисти
    """
    fill_prop = QColor(0, 0, 255, 155)

    def __init__(self, _fill_prop):
        self.fill_prop = _fill_prop

    def apply_props(self, painter):
        """
        Перезаписываем применение всех свойств к Painter'у для кисти
        :param painter: класс Painter
        """
        painter.fill_prop = self.fill_prop
