from typing import ClassVar
from data import Entry, Database
import os

basedir = os.getcwd()


class Settings(Database):
    def __init__(self):
        label = "settings"
        super().__init__(label)
        self.label = label

    def set_threshold_stock(self, value):
        self.table["threshold_stock"] = value

    def get_threshold_stock(self):
        return self.table["threshold_stock"]