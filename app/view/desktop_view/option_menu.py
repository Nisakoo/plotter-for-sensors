from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QComboBox, QVBoxLayout


class OptionMenu(QWidget):

    item_changed = pyqtSignal()

    def __init__(self, default_value: str):
        super(OptionMenu, self).__init__()

        self.__default_value = default_value
        self.__selected = None

        self.__menu = QComboBox()
        self.__menu.addItem(self.__default_value, userData=None)

        self.__menu.currentIndexChanged.connect(self.current_index_changed)

        self.__layout = QVBoxLayout()
        self.__layout.addWidget(self.__menu)

        self.setLayout(self.__layout)

    @property
    def selected_item(self) -> Any:
        return self.__selected
    
    def update(self, labels: list, items: list) -> None:
        self.__menu.clear()

        if (len(labels) > 0) and (len(labels) == len(items)):
            for label, item in zip(labels, items):
                self.__menu.addItem(label, userData=item)
        else:
            self.__menu.addItem(self.__default_value, userData=None)

    def current_index_changed(self, index: int) -> None:
        self.__selected = self.__menu.itemData(index)
        self.item_changed.emit()