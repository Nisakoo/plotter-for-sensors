from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication

from app.view.desktop_view.main_window import MainWindow


class DesktopView(QApplication):
    def __init__(self, *argv):
        super(DesktopView, self).__init__(*argv)

        self.__main_window = MainWindow()
        self.__main_window.show()

        self.exec()