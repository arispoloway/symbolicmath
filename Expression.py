from abc import ABC, abstractmethod
from math import sin
import logging

logging.basicConfig()
log = logging.getLogger()

class Expression(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def evaluate(self, **kwargs):
        pass

    def get_value(self):
        return None

    @abstractmethod
    def __repr__(self):
        pass



