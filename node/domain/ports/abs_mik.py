from abc import ABC, abstractmethod


class AbstractMik(ABC):
    tank_wrapper = None

    def __init__(self, path=None):
        self._path = path
        self._setting = {}

    @abstractmethod
    def get_settings(self):
        pass

    @abstractmethod
    def get_values_from_key(self, key, fields=None):
        pass
