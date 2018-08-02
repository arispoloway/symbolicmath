from abc import ABC
from functools import reduce
from itertools import chain
from collections import Counter
from math import sin, cos, acos, asin, pow, log, e

from expression.Expression import Expression
from expression.Value import Value
from expression.Variable import Variable
from expression.Utils import reduce_all
from parsing.Utils import possibly_parse_literal


class Function(Expression, ABC):
    def __init__(self, func, *expressions):
        super().__init__()
        self._func = func
        self._expressions = tuple(map(possibly_parse_literal, expressions))

    def get_expressions(self):
        return self._expressions

    def evaluate(self, **kwargs):
        evaluated = list(map(lambda x: x.evaluate(**kwargs), self._expressions))
        if all(e.get_numeric_value() is not None for e in evaluated):
            return Value(self._func(*map(lambda x: x.get_numeric_value(), evaluated)))
        else:
            return type(self)(*evaluated)

    def get_func(self):
        return self._func

    def __eq__(self, other):
        return isinstance(other, type(self)) and \
               set(self.get_expressions()) == set(other.get_expressions())

    def __hash__(self):
        return hash((type(self), self.get_expressions()))


class Sin(Function):
    def __init__(self, expr):
        super().__init__(sin, expr)

    def reduce(self):
        expr = self.get_expressions()[0]
        if isinstance(expr, Asin):
            return expr.get_expressions()[0].reduce()
        return Sin(expr.reduce())

    def __repr__(self):
        return 'sin({})'.format(self._expressions[0].__repr__())

class Cos(Function):
    def __init__(self, expr):
        super().__init__(cos, expr)

    def reduce(self):
        expr = self.get_expressions()[0]
        if isinstance(expr, Acos):
            return expr.get_expressions()[0].reduce()
        return Cos(expr.reduce())

    def __repr__(self):
        return 'cos({})'.format(self._expressions[0].__repr__())

class Asin(Function):
    def __init__(self, expr):
        super().__init__(asin, expr)

    def reduce(self):
        expr = self.get_expressions()[0]
        if isinstance(expr, Sin):
            return expr.get_expressions()[0].reduce()
        return Asin(expr.reduce())

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

    def __repr__(self):
        return 'acos({})'.format(self._expressions[0].__repr__())

class Negate(Function):
    def __init__(self, expr):
        super().__init__(lambda x: -x, expr)

    def reduce(self):
        expr = self.get_expressions()[0]
        # Maybe not do this?
        if isinstance(expr, Value):
            return Value(-expr.get_numeric_value())
        return -(expr.reduce())

    def __repr__(self):
        return '-{}'.format(self._expressions[0].__repr__())

class Add(Function):
    def __init__(self, *expressions):
        super().__init__(lambda *l: reduce(lambda x, y: x+y, l), *expressions)
        if len(expressions) < 2:
            raise ValueError('Not enough expressions')

    def reduce(self):
        exprs = reduce_all(self.get_expressions())

        add_terms = []
        others = []
        for expr in exprs:
            if isinstance(expr, Add):
                add_terms += expr.get_expressions()
            else:
                others.append(expr)

        if add_terms:
            multiply_terms = Add(*add_terms).reduce().get_expressions()


        total = [*others, *add_terms]
        values = [x.get_numeric_value() for x in total if isinstance(x, Value)] + [0]
        value = Value(self.get_func()(*values))
        others = tuple(filter(lambda x: not isinstance(x, Value), total))

        counts = Counter(others)
        others = []
        for term in counts:
            freq = counts[term]
            if freq == 1:
                others.append(term)
            else:
                others.append(Value(freq) * term)

        if len(others) == 0:
            return value

        if value == Value(0):
            if len(others) == 1:
                return others[0]
            return Add(*others)

        return Add(value, *others)

    def __repr__(self):
        return '(' + \
               '+'.join(x.__repr__() for x in self.get_expressions()) + \
               ')'

class Subtract(Function):
    def __init__(self, expr1, expr2):
        super().__init__(lambda a, b: a-b, expr1, expr2)

    def reduce(self):
        exprs = reduce_all(self.get_expressions())
        if exprs[0] == Value(0):
            return -exprs[1]
        if exprs[1] == Value(0):
            return exprs[0]
        if isinstance(exprs[0], Value) and isinstance(exprs[1], Value):
            return Value(exprs[0].get_numeric_value() - exprs[1].get_numeric_value())
        return Subtract(exprs[0], exprs[1])

    def __repr__(self):
        return '({}-{})'.format(self._expressions[0].__repr__(), self._expressions[1].__repr__())

class Divide(Function):
    def __init__(self, numer, denom):
        super().__init__(lambda a, b: a/b, numer, denom)

    def reduce(self):
        exprs = reduce_all(self.get_expressions())
        if exprs[1] == Value(1):
            return exprs[0]
        if exprs[1] == Value(-1):
            return (-exprs[0])
        return Divide(exprs[0], exprs[1])

    def __repr__(self):
        return '(({})/({}))'.format(self._expressions[0].__repr__(), self._expressions[1].__repr__())

class Multiply(Function):
    def __init__(self, *expressions):
        super().__init__(lambda *l: reduce(lambda x, y: x*y, l), *expressions)
        if len(expressions) < 2:
            raise ValueError('Not enough expressions')

    def reduce(self):
        exprs = reduce_all(self.get_expressions())

        multiply_terms = []
        others = []
        for expr in exprs:
            if isinstance(expr, Multiply):
                multiply_terms += expr.get_expressions()
            else:
                others.append(expr)

        if multiply_terms:
            multiply_terms = Multiply(*multiply_terms).reduce().get_expressions()


        total = [*others, *multiply_terms]
        values = [x.get_numeric_value() for x in total if isinstance(x, Value)] + [1]
        value = Value(self.get_func()(*values))
        others = tuple(filter(lambda x: not isinstance(x, Value), total))

        counts = Counter(others)
        others = []
        for term in counts:
            freq = counts[term]
            if freq == 1:
                others.append(term)
            else:
                others.append(term ^ freq)

        if value == Value(0):
            return value

        if len(others) == 0:
            return value

        if value == Value(1):
            if len(others) == 1:
                return others[0]
            return Multiply(*others)
        if value == Value(-1):
            if len(others) == 1:
                return -others[0]
            return -Multiply(others)


        else:
            return Multiply(value, *others)



    def __repr__(self):
        return '('+ '*'.join(x.__repr__() for x in self.get_expressions()) + ')'


class Power(Function):
    def __init__(self, base, exponent):
        super().__init__(lambda x, y: pow(x, y), base, exponent)
        _, exp = self.get_expressions()
        if not isinstance(exp, Value):
            raise ValueError('Invalid exponent')

    def reduce(self):
        base, exp = reduce_all(self.get_expressions())
        if exp == Value(1):
            return base
        if exp == Value(0):
            return Value(1)
        if isinstance(base, Value):
            return Value(self.get_func()(base.get_numeric_value(), exp.get_numeric_value()))
        return self

    def __repr__(self):
        exprs = self.get_expressions()
        return '({})^({})'.format(exprs[0], exprs[1])

class Exponent(Function):
    def __init__(self, base, exponent):
        super().__init__(lambda x, y: pow(x, y), base, exponent)
        b, _ = self.get_expressions()
        if not isinstance(b, Value):
            raise ValueError('Invalid base')

    def reduce(self):
        #TODO add reducers with log and stuff
        return self

    def __repr__(self):
        exprs = self.get_expressions()
        return '({})^({})'.format(exprs[0], exprs[1])

class Log(Function):
    def __init__(self, n, base=e):
        super().__init__(lambda x, y: log(n, base), n, base)

    def reduce(self):
        return self

    def __repr__(self):
        exprs = self.get_expressions()
        return '({})^({})'.format(exprs[0].__repr__(), exprs[1].__repr__())
