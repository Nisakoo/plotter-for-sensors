from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QCheckBox

from app.view.desktop_view.option_menu import OptionMenu


class Toolbar(QWidget):
    def __init__(self):
        super(Toolbar, self).__init__()

        self.ports_menu = OptionMenu("Порт не выбран")
        self.sensors_menu = OptionMenu("Датчик не выбран")

        self.refresh_ports_btn = QPushButton("Обновить")

        self.toggle_reading_btn = QPushButton("Читать")
        self.toggle_reading_btn.setCheckable(True)

        self.save_to_file_checkbox = QCheckBox("Сохранять в файл")

        self.__layout = QHBoxLayout()
        self.__layout.addWidget(self.ports_menu)
        self.__layout.addWidget(self.refresh_ports_btn)
        self.__layout.addWidget(self.sensors_menu)
        self.__layout.addWidget(self.toggle_reading_btn)
        self.__layout.addWidget(self.save_to_file_checkbox)

        self.setFixedHeight(60)
        self.setLayout(self.__layout)