from abc import ABC, abstractmethod
from functools import reduce
from math import sin, cos, acos, asin, pow, log, e

from expression.SimplifiableExpression import SimplifiableExpression
from expression.Value import Value
from expression.Utils import simplify_all
from parsing.Utils import possibly_parse_literal


class Function(SimplifiableExpression, ABC):
    @abstractmethod
    def __repr__(self):
        pass

    def __init__(self, func, *expressions, commute=False):
        super().__init__()
        self._func = func
        self._expressions = tuple(map(possibly_parse_literal, expressions))
        self._commute = commute

    # TODO: fix bc this encourages bad things, should have individual methods on subclasses
    def get_expressions(self):
        return self._expressions

    def evaluate(self, **kwargs):
        evaluated = list(map(lambda x: x.evaluate(**kwargs), self._expressions))
        if all(expr.get_numeric_value() is not None for expr in evaluated):
            return Value(self._func(*map(lambda x: x.get_numeric_value(), evaluated)))
        else:
            return type(self)(*evaluated)

    def simplify_sub_expressions(self, whitelist=None):
        return type(self)(*simplify_all(self._expressions))

    def get_func(self):
        return self._func

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if self._commute:
            return set(self.get_expressions()) == set(other.get_expressions())
        return self.get_expressions() == other.get_expressions()

    def __hash__(self):
        return hash((type(self), self.get_expressions()))


class Sin(Function):
    def __init__(self, expr):
        super().__init__(sin, expr)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import ValueOnlySimplifier
        from expression.simplifier.TrigSimplifiers import SinAsinSimplifier
        return [SinAsinSimplifier(), ValueOnlySimplifier()]

    def __repr__(self):
        return 'sin({})'.format(self._expressions[0].__repr__())


class Cos(Function):
    def __init__(self, expr):
        super().__init__(cos, expr)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import ValueOnlySimplifier
        from expression.simplifier.TrigSimplifiers import CosAcosSimplifier
        return [CosAcosSimplifier(), ValueOnlySimplifier()]

    def __repr__(self):
        return 'cos({})'.format(self._expressions[0].__repr__())


class Asin(Function):
    def __init__(self, expr):
        super().__init__(asin, expr)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import ValueOnlySimplifier
        from expression.simplifier.TrigSimplifiers import AsinSinSimplifier
        return [AsinSinSimplifier(), ValueOnlySimplifier()]

    def __repr__(self):
        return 'asin({})'.format(self._expressions[0].__repr__())


class Acos(Function):
    def __init__(self, expr):
        super().__init__(acos, expr)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import ValueOnlySimplifier
        from expression.simplifier.TrigSimplifiers import AcosCosSimplifier
        return [AcosCosSimplifier(), ValueOnlySimplifier()]

    def __repr__(self):
        return 'acos({})'.format(self._expressions[0].__repr__())


class Negate(Function):
    def __init__(self, expr):
        super().__init__(lambda x: -x, expr)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import ValueOnlySimplifier
        return [ValueOnlySimplifier()]

    def __repr__(self):
        return '-{}'.format(self._expressions[0].__repr__())


class Add(Function):
    def __init__(self, *expressions):
        super().__init__(lambda *x: sum(x), *expressions)
        if len(expressions) < 2:
            raise ValueError('Not enough expressions')

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import (
            ValueOnlySimplifier,
        )
        from expression.simplifier.AddSimplifiers import (
            AddCombineTermsSimplifier,
            AddCombineValuesSimplifier,
            AddNestedAddSimplifier,
        )
        return [ValueOnlySimplifier(),
                AddNestedAddSimplifier(),
                AddCombineValuesSimplifier(),
                AddCombineTermsSimplifier(), ]

    def __eq__(self, other):
        return isinstance(other, Add) and set(self.get_expressions()) == set(other.get_expressions())

    def __hash__(self):
        return hash((type(self), self.get_expressions()))

    def __repr__(self):
        return '(' + \
               '+'.join(x.__repr__() for x in self.get_expressions()) + \
               ')'


class Subtract(Function):
    def __init__(self, expr1, expr2):
        super().__init__(lambda a, b: a - b, expr1, expr2)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import ValueOnlySimplifier
        from expression.simplifier.SubtractSimplifiers import SubtractWithZeroSimplifier
        return [ValueOnlySimplifier(), SubtractWithZeroSimplifier()]

    def __repr__(self):
        return '({}-{})'.format(self._expressions[0].__repr__(), self._expressions[1].__repr__())


class Divide(Function):
    def __init__(self, numer, denom):
        super().__init__(lambda a, b: a / b, numer, denom)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import ValueOnlySimplifier
        from expression.simplifier.DivideSimplifiers import DivideByOneSimplifier
        return [ValueOnlySimplifier(), DivideByOneSimplifier()]

    def __repr__(self):
        return '(({})/({}))'.format(self._expressions[0].__repr__(), self._expressions[1].__repr__())


class Multiply(Function):
    def __init__(self, *expressions):
        super().__init__(lambda *l: reduce(lambda x, y: x * y, l), *expressions, commute=True)
        if len(expressions) < 2:
            raise ValueError('Not enough expressions')

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import (
            ValueOnlySimplifier,
        )
        from expression.simplifier.MultiplySimplifiers import (
            MultiplyCombineValuesSimplifier,
            MultiplyCombineTermsSimplifier,
            MultiplyNestedMultiplySimplifier,
        )
        return [ValueOnlySimplifier(),
                MultiplyNestedMultiplySimplifier(),
                MultiplyCombineValuesSimplifier(),
                MultiplyCombineTermsSimplifier(), ]

    def __repr__(self):
        return '(' + '*'.join(x.__repr__() for x in self.get_expressions()) + ')'


class Exponent(Function):
    def __init__(self, base, exponent):
        super().__init__(pow, base, exponent)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import ValueOnlySimplifier
        from expression.simplifier.PowerSimplifiers import PowerOfZeroSimplifier
        from expression.simplifier.PowerSimplifiers import PowerOfOneSimplifier
        return [ValueOnlySimplifier(), PowerOfOneSimplifier(), PowerOfZeroSimplifier()]

    def __repr__(self):
        exprs = self.get_expressions()
        return '({})^({})'.format(exprs[0], exprs[1])


class Log(Function):
    def __init__(self, n, base=e):
        super().__init__(log, n, base)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import ValueOnlySimplifier
        return [ValueOnlySimplifier()]

    def __repr__(self):
        exprs = self.get_expressions()
        return 'Log(n={}, b={})'.format(exprs[0].__repr__(), exprs[1].__repr__())
