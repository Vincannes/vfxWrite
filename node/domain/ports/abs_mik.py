from abc import ABC, abstractmethod


class AbstractMik(ABC):

    def __init__(self, path=None):
        self._path = path
        self._setting = {}

    @abstractmethod
    def get_settings(self):
        pass
