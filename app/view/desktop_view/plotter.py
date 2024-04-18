import numpy as np

from PyQt6.QtWidgets import QVBoxLayout, QWidget

import pyqtgraph as pg


class Plotter(QWidget):
    def __init__(self):
        super(Plotter, self).__init__()

        self.__plotter = pg.PlotWidget()
        self.__plotter.setBackground("w")
        self.__plotter.showGrid(y=True)

        self.__line = self.__plotter.plot(
            [], [], 
            pen=pg.mkPen("b", width=3)
        )

        self.__layout = QVBoxLayout()
        self.__layout.addWidget(self.__plotter)

        self.setLayout(self.__layout)

    def update(self, data) -> None:
        self.__line.setData(np.linspace(0, 10, len(data)), data)