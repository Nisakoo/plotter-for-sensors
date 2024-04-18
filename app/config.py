import os
import pickle

from app.readers.sensor import Sensor


class Config:

    __SENSORS = dict()
    __CONFIG_FILENAME = "config.pk"
    
    @classmethod
    def load(cls):
        if os.path.exists(cls.__CONFIG_FILENAME):
            with open(cls.__CONFIG_FILENAME, "rb") as config_file:
                cls.__SENSORS = pickle.load(config_file)

    @classmethod
    def save(cls):
        with open(cls.__CONFIG_FILENAME, "wb") as config_file:
            pickle.dump(cls.__SENSORS, config_file, protocol=pickle.HIGHEST_PROTOCOL)
    
    @classmethod
    def get_by_id(cls, sensor_id):
        if cls.has(sensor_id):
            return cls.__SENSORS[sensor_id]
        
        return None
    
    @classmethod
    def update(cls, sensor: Sensor):
        cls.__SENSORS[sensor.id] = sensor
        cls.save()

    @classmethod
    def has(cls, sensor_id):
        return (sensor_id in cls.__SENSORS)