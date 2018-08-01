from Expression import Expression
from abc import ABC, abstractmethod
from math import sin
from Value import Value


class Operation(Expression, ABC):
    def __init__(self, func, *expressions):
        super().__init__()
        self._func = func
        self._expressions = expressions

    def evaluate(self, **kwargs):
        evaluated = list(map(lambda x: x.evaluate(**kwargs), self._expressions))
        if all(e.get_value() is not None for e in evaluated):
            return Value(self._func(*map(lambda x: x.get_value(), evaluated)))
        else:
            return self.new_operation(*evaluated)

    @abstractmethod
    def new_operation(self, *evaluated):
        pass

class Sin(Operation):
    def __init__(self, expr):
        super().__init__(sin, expr)

    def new_operation(self, *evaluated):
        return Sin(evaluated[0])

    def __repr__(self):
        return 'sin({})'.format(self._expressions[0].__repr__())

class Add(Operation):
    def __init__(self, expr1, expr2):
        super().__init__(lambda a, b: a+b, expr1, expr2)

    def new_operation(self, *evaluated):
        return Add(evaluated[0], evaluated[1])

    def __repr__(self):
        return '{}+{}'.format(self._expressions[0].__repr__(), self._expressions[1].__repr__())

