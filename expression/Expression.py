import logging
from abc import ABC, abstractmethod

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

    def reduce(self):
        return self

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    def __add__(self, other):
        import expression.Function
        return expression.Function.Add(self, other)

    def __mul__(self, other):
        import expression.Function
        return expression.Function.Multiply(self, other)

    def __sub__(self, other):
        import expression.Function
        return expression.Function.Subtract(self, other)

    def __neg__(self):
        import expression.Function
        return expression.Function.Negate(self)



