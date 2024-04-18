import re

from collections import deque

from PyQt6.QtCore import QObject, pyqtSignal

from app.readers.sensor import Sensor

from app.config import *


class SensorsReader(QObject):

    __HISTORY_SIZE = 100
    __VALID_PATTERN_1 = re.compile(r"^[*][a-zA-Z0-9]+[:][a-zA-Z0-9]+[:][0-9.]+[#]$")
    __VALID_PATTERN_2 = re.compile(r"^[*][a-zA-Z0-9]+[:][a-zA-Z0-9]+[#]$")

    sensor_connected = pyqtSignal()

    def __init__(self):
        super(SensorsReader, self).__init__()

        self.__history: dict[str, deque] = dict()
        self.__last_data: dict[str, float] = dict()
        self.__connected_sensors = list()
        self.__sensors_connected = False

    def start_reading(self):
        self.__sensors_connected = False
        self.__last_data = dict()
        self.__connected_sensors = list()

    def update(self, raw_data):
        raw_data = self.prepare_data(raw_data)

        if self.is_valid(raw_data):
            data = list(self.extract_data(raw_data))
            sensor_id = data[0]

            if not Config.has(sensor_id):
                new_sensor = Sensor(id=sensor_id)

                if len(data) == 2:
                    new_sensor.name = data[1]

                Config.update(new_sensor)

            if Config.get_by_id(sensor_id) not in self.__connected_sensors:
                self.__connected_sensors.append(Config.get_by_id(sensor_id))
            else:
                if not self.__sensors_connected:
                    self.__sensors_connected = True
                    self.sensor_connected.emit()

            if sensor_id in self.__history:
                if len(data) == 3:
                    data[2] = Config.get_by_id(sensor_id).to_scale([data[2]])[0]

                    self.__history[sensor_id].append(data[2])

                    if sensor_id in self.__last_data:
                        self.__last_data = dict()
                    else:
                        self.__last_data[Config.get_by_id(sensor_id).name] = data[2]
            else:
                self.__history[sensor_id] = deque([], maxlen=self.__HISTORY_SIZE)

    def get_values(self, sensor_id):
        if sensor_id in self.__history:
            return list(self.__history[sensor_id])
        
        return list()
    
    def is_all_sensor_connected(self) -> bool:
        return self.__sensors_connected
    
    def get_last_data(self) -> dict:
        if self.__sensors_connected:
            if len(self.__connected_sensors) == len(self.__last_data):
                return self.__last_data
        
        return dict()
    
    def get_available_sensors(self):
        sensor_ids = self.__history.keys()
        sensors = list()

        for id in sensor_ids:
            sensors.append(self.get_sensor_by_id(id))

        return sensors
    
    def get_sensor_by_id(self, sensor_id):
        if Config.has(sensor_id):
            return Config.get_by_id(sensor_id)
        
        return Sensor(id=sensor_id)
    
    def prepare_data(self, raw_data: str) -> str:
        return raw_data.rstrip("\r\n")
    
    def is_valid(self, data):
        if re.match(self.__VALID_PATTERN_1, data):
            return True
        
        if re.match(self.__VALID_PATTERN_2, data):
            return True

        return False
    
    def extract_data(self, raw_data: str) -> tuple:
        raw_data = raw_data[1:-1]
        splitted_data = raw_data.split(":")

        sensor_id = splitted_data[0]
        info = splitted_data[1]

        if len(splitted_data) == 3:
            return sensor_id, info, float(splitted_data[2])

        return sensor_id, info