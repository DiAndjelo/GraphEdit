import sys
from PyQt5.QtWidgets import QApplication
from Editor.Settings import Settings

if __name__ == '__main__':
    app = QApplication([])
    start = Settings()
    sys.exit(app.exec_())
