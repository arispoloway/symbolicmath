from Expression import Expression
from abc import ABC, abstractmethod
from math import sin, cos, acos, asin
from functools import reduce
from Value import Value


class Function(Expression, ABC):
    def __init__(self, func, *expressions):
        super().__init__()
        self._func = func
        self._expressions = expressions

    def get_expressions(self):
        return self._expressions

    def evaluate(self, **kwargs):
        evaluated = list(map(lambda x: x.evaluate(**kwargs), self._expressions))
        if all(e.get_value() is not None for e in evaluated):
            return Value(self._func(*map(lambda x: x.get_value(), evaluated)))
        else:
            return self.new_operation(*evaluated)

    def get_func(self):
        return self._func

    @abstractmethod
    def new_operation(self, *evaluated):
        pass

class Sin(Function):
    def __init__(self, expr):
        super().__init__(sin, expr)

    def new_operation(self, *evaluated):
        return Sin(evaluated[0])

    def reduce(self):
        expr = self.get_expressions()[0]
        if isinstance(expr, Asin):
            return expr.get_expressions()[0].reduce()
        return Sin(expr.reduce())

    def __repr__(self):
        return 'sin({})'.format(self._expressions[0].__repr__())

    def __eq__(self, other):
        return isinstance(other, Sin) and \
               self.get_expressions() == other.get_expressions()

    def __hash__(self):
        return hash(('sin', self.get_expressions()))

class Cos(Function):
    def __init__(self, expr):
        super().__init__(cos, expr)

    def new_operation(self, *evaluated):
        return Cos(evaluated[0])

    def reduce(self):
        expr = self.get_expressions()[0]
        if isinstance(expr, Acos):
            return expr.get_expressions()[0].reduce()
        return Cos(expr.reduce())

    def __eq__(self, other):
        return isinstance(other, Cos) and \
               self.get_expressions() == other.get_expressions()

    def __hash__(self):
        return hash(('cos', self.get_expressions()))

    def __repr__(self):
        return 'cos({})'.format(self._expressions[0].__repr__())

class Asin(Function):
    def __init__(self, expr):
        super().__init__(asin, expr)

    def new_operation(self, *evaluated):
        return Asin(evaluated[0])

    def reduce(self):
        expr = self.get_expressions()[0]
        if isinstance(expr, Sin):
            return expr.get_expressions()[0].reduce()
        return Asin(expr.reduce())

    def __eq__(self, other):
        return isinstance(other, Asin) and \
               self.get_expressions() == other.get_expressions()

    def __hash__(self):
        return hash(('asin', self.get_expressions()))

    def __repr__(self):
        return 'asin({})'.format(self._expressions[0].__repr__())

class Acos(Function):
    def __init__(self, expr):
        super().__init__(acos, expr)

    def new_operation(self, *evaluated):
        return Acos(evaluated[0])

    def reduce(self):
        expr = self.get_expressions()[0]
        if isinstance(expr, Cos):
            return expr.get_expressions()[0].reduce()
        return Acos(expr.reduce())

    def __eq__(self, other):
        return isinstance(other, Acos) and \
               self.get_expressions() == other.get_expressions()

    def __hash__(self):
        return hash(('acos', self.get_expressions()))

    def __repr__(self):
        return 'acos({})'.format(self._expressions[0].__repr__())

class Negate(Function):
    def __init__(self, expr):
        super().__init__(lambda x: -x, expr)

    def new_operation(self, *evaluated):
        return Negate(evaluated[0])

    def reduce(self):
        expr = self.get_expressions()[0]
        # Maybe not do this?
        if isinstance(expr, Value):
            return Value(-expr.get_value())
        return -(expr.reduce())

    def __eq__(self, other):
        return isinstance(other, Negate) and \
               self.get_expressions() == other.get_expressions()

    def __hash__(self):
        return hash(('negate', self.get_expressions()))

    def __repr__(self):
        return '-{}'.format(self._expressions[0].__repr__())

class Add(Function):
    def __init__(self, *expressions):
        super().__init__(lambda *l: reduce(lambda x, y: x+y, l), *expressions)

    def new_operation(self, *evaluated):
        return Add(*evaluated)

    def reduce(self):
        exprs = list(map(lambda x: x.reduce(), self.get_expressions()))

        values = list(filter(lambda x: isinstance(x, Value), exprs))
        value = Value(self.get_func()(0, *(x.get_value() for x in values)))

        others = list(filter(lambda x: not isinstance(x, Value), exprs))

        if len(others) == 0:
            return value

        if value == Value(0):
            if len(others) == 1:
                return others[0]
            return Add(*others)

        return Add(value, *others)

        return Add(value, *others)


    def __eq__(self, other):
        return isinstance(other, Add) and \
               set(self.get_expressions()) == set(other.get_expressions())

    def __hash__(self):
        return hash(('add', self.get_expressions()))

    def __repr__(self):
        return '+'.join(x.__repr__() for x in self.get_expressions())

class Subtract(Function):
    def __init__(self, expr1, expr2):
        super().__init__(lambda a, b: a-b, expr1, expr2)

    def new_operation(self, *evaluated):
        return Subtract(evaluated[0], evaluated[1])

    def reduce(self):
        exprs = self.get_expressions()
        if exprs[0] == Value(0):
            return (-exprs[1]).reduce()
        if exprs[1] == Value(0):
            return exprs[0].reduce()

    def __eq__(self, other):
        return isinstance(other, Subtract) and \
               self.get_expressions() == other.get_expressions()

    def __hash__(self):
        return hash(('subtract', self.get_expressions()))

    def __repr__(self):
        return '{}-{}'.format(self._expressions[0].__repr__(), self._expressions[1].__repr__())

class Multiply(Function):
    def __init__(self, *expressions):
        super().__init__(lambda *l: reduce(lambda x, y: x*y, l), *expressions)

    def new_operation(self, *evaluated):
        return Multiply(*evaluated)

    def reduce(self):
        exprs = list(map(lambda x: x.reduce(), self.get_expressions()))

        values = list(filter(lambda x: isinstance(x, Value), exprs))
        value = Value(self.get_func()(1, *(x.get_value() for x in values)))

        others = list(filter(lambda x: not isinstance(x, Value), exprs))

        if len(others) == 0:
            return value

        if value == Value(1):
            if len(others) == 1:
                return others[0]
            return Multiply(*others)
        if value == Value(0):
            return Value(0)
        if value == Value(-1):
            if len(others) == 1:
                return -others[0]
            return -Multiply(others)

        return Multiply(value, *others)

    def __eq__(self, other):
        return isinstance(other, Multiply) and \
               set(self.get_expressions()) == set(other.get_expressions())

    def __hash__(self):
        return hash(('multiply', self.get_expressions()))

    def __repr__(self):
        return '*'.join(x.__repr__() for x in self.get_expressions())
