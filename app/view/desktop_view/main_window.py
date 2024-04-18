from PyQt6.QtCore import QTimer, pyqtSlot, QIODevice
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QWidget, QFileDialog

from app.view.desktop_view.toolbar import Toolbar
from app.view.desktop_view.plotter import Plotter
from app.view.desktop_view.values_setting_menu import ValuesSettingMenu

from app.readers.sensors_reader import SensorsReader
from app.readers.sensor import Sensor
from app.writers.file_writer import FileWriter


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Plotter v2.0")

        self.__reader = SensorsReader()
        self.__reader.sensor_connected.connect(self.update_sensors_list)

        self.__writer = FileWriter()

        self.__toolbar = Toolbar()
        self.__plotter = Plotter()
        self.__values_setting_menu = ValuesSettingMenu()

        self.__toolbar.refresh_ports_btn.clicked.connect(self.update_ports_list)
        self.__toolbar.toggle_reading_btn.clicked.connect(self.toggle_reading_callback)
        self.__toolbar.sensors_menu.item_changed.connect(self.update_plotter)
        self.__toolbar.sensors_menu.item_changed.connect(self.set_sensor_to_setting_menu)

        self.__plotter_timer = QTimer()
        self.__plotter_timer.setInterval(10)
        self.__plotter_timer.timeout.connect(self.update_plotter)

        self.__values_setting_menu.data_updated.connect(self.update_sensors_list)

        self.__serial = QSerialPort()
        self.__serial.setBaudRate(115200)
        self.__serial.readyRead.connect(self.read_serial)

        self.__layout = QGridLayout()
        self.__layout.addWidget(self.__toolbar, 1, 1, 1, 2)
        self.__layout.addWidget(self.__plotter, 2, 1)
        self.__layout.addWidget(self.__values_setting_menu, 2, 2)

        self.__container = QWidget()
        self.__container.setLayout(self.__layout)

        self.setCentralWidget(self.__container)

    @pyqtSlot()
    def read_serial(self):
        while self.__serial.canReadLine():
            raw_data = self.__serial.readLine()
            raw_data = raw_data.data().decode()

            self.__reader.update(raw_data)
            last_data = self.__reader.get_last_data()

            if last_data:
                self.__writer.add_data(last_data)

    def serial_connect(self, port):
        self.serial_disconnect()

        self.__serial.setPort(port)
        self.__serial.open(QIODevice.OpenModeFlag.ReadOnly)

    def serial_disconnect(self):
        if self.__serial.isOpen():
            self.__serial.close()

    def toggle_reading_callback(self, checked):
        is_checked = False

        if checked:
            selected_port = self.__toolbar.ports_menu.selected_item

            if selected_port is not None:
                if self.__toolbar.save_to_file_checkbox.isChecked():
                    filename, _ = QFileDialog.getSaveFileName(
                        self, filter="CSV (*.csv)",
                        directory="data.csv"
                    )
                    
                    if filename:
                        self.__writer.set_file(filename)

                self.serial_connect(selected_port)
                self.__reader.start_reading()
                self.__plotter_timer.start()

                self.__toolbar.toggle_reading_btn.setText("Стоп")
                is_checked = True
        else:
            self.serial_disconnect()
            self.__writer.close_file()
            self.__plotter_timer.stop()
            self.__toolbar.toggle_reading_btn.setText("Читать")

        self.__toolbar.toggle_reading_btn.setChecked(is_checked)

    def update_sensors_list(self):
        sensors = self.__reader.get_available_sensors()
        labels = [sensor.name for sensor in sensors]

        self.__toolbar.sensors_menu.update(labels, sensors)

    def update_ports_list(self):
        ports = QSerialPortInfo.availablePorts()
        labels = [port.portName() for port in ports]

        self.__toolbar.ports_menu.update(labels, ports)

    def update_plotter(self) -> None:
        selected_sensor = self.__toolbar.sensors_menu.selected_item

        if selected_sensor is not None:
            self.__plotter.update(self.__reader.get_values(selected_sensor.id))

    def set_sensor_to_setting_menu(self):
        selected_sensor = self.__toolbar.sensors_menu.selected_item

        if selected_sensor is not None:
            self.__values_setting_menu.set_sensor(selected_sensor.id)