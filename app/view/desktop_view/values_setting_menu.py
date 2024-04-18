from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import Qt, QLocale, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QCheckBox

from app.readers.sensor import Sensor

from app.config import *


class ValuesSettingMenu(QWidget):

    data_updated = pyqtSignal()

    def __init__(self):
        super(ValuesSettingMenu, self).__init__()

        self.setFixedWidth(150)

        self.__sensor: Sensor = None

        self.__name = QLineEdit()
        self.__rescale_checkbox = QCheckBox("Переводить")
        self.__min_value = QLineEdit()
        self.__max_value = QLineEdit()
        self.__min_scaled_value = QLineEdit()
        self.__max_scaled_value = QLineEdit()
        self.__bias_value = QLineEdit()
        self.__save_btn = QPushButton(text="Применить")
        self.__save_btn.clicked.connect(self.save_data)

        self.__double_validator = QDoubleValidator()

        self.__min_value.setValidator(self.__double_validator)
        self.__max_value.setValidator(self.__double_validator)
        self.__min_scaled_value.setValidator(self.__double_validator)
        self.__max_scaled_value.setValidator(self.__double_validator)
        self.__bias_value.setValidator(self.__double_validator)

        self.__layout = QVBoxLayout()
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.__layout.addWidget(QLabel(text="Название:"))
        self.__layout.addWidget(self.__name)
        self.__layout.addWidget(self.__rescale_checkbox)
        self.__layout.addWidget(QLabel(text="Макс. значение:"))
        self.__layout.addWidget(self.__max_value)
        self.__layout.addWidget(QLabel(text="Мин. значение:"))
        self.__layout.addWidget(self.__min_value)
        self.__layout.addWidget(QLabel(text="Новый макс.:"))
        self.__layout.addWidget(self.__max_scaled_value)
        self.__layout.addWidget(QLabel(text="Новый мин.:"))
        self.__layout.addWidget(self.__min_scaled_value)
        self.__layout.addWidget(QLabel(text="Смещение:"))
        self.__layout.addWidget(self.__bias_value)
        self.__layout.addWidget(self.__save_btn)

        self.setLayout(self.__layout)

    def set_sensor(self, sensor_id: str) -> None:
        if Config.has(sensor_id):
            self.__sensor = Config.get_by_id(sensor_id)

            self.__name.setText(self.__sensor.name)
            self.__rescale_checkbox.setChecked(self.__sensor.rescale)
            self.__max_value.setText(str(self.__sensor.max_value))
            self.__min_value.setText(str(self.__sensor.min_value))
            self.__max_scaled_value.setText(str(self.__sensor.scale_max))
            self.__min_scaled_value.setText(str(self.__sensor.scale_min))
            self.__bias_value.setText(str(self.__sensor.bias))

    def save_data(self) -> None:
        if self.__sensor is not None:
            self.__sensor.name = self.__name.text()
            self.__sensor.rescale = self.__rescale_checkbox.isChecked()
            self.__sensor.max_value = self._get_float(self.__max_value.text())
            self.__sensor.min_value = self._get_float(self.__min_value.text())
            self.__sensor.scale_max = self._get_float(self.__max_scaled_value.text())
            self.__sensor.scale_min = self._get_float(self.__min_scaled_value.text())
            self.__sensor.bias = self._get_float(self.__bias_value.text())

            Config.update(self.__sensor)

            self.data_updated.emit()

    def _get_float(self, s: str) -> float:
        return float(s.replace(",", "."))