from PyQt5.QtWidgets import QMainWindow
from Forms.SettingsForm import SettingsForm


class Settings(QMainWindow):
    """
    Инициализация формы настроек редактора
    """
    def __init__(self):
        super().__init__()
        self.form = SettingsForm()
        self.form.setGeometry(600, 200, 250, 600)
        self.form.show()
