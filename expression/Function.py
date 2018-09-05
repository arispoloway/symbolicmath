from abc import ABC, abstractmethod
from functools import reduce
from math import sin, cos, acos, asin, pow, log, e

from expression.SimplifiableExpression import SimplifiableExpression
from expression.Value import Value
from expression.Utils import simplify_all
from parsing.Utils import possibly_parse_literal


class Function(SimplifiableExpression, ABC):
    """
    An abstract class to generalize the idea of a function acting on sub expressions
    """
    @abstractmethod
    def __repr__(self):
        pass

    def __init__(self, func, *expressions, commute=False):
        """
        Args:
            func: The python function that acts on numeric values
            *expressions: The list of expressions the func acts on
            commute: Whether or not the order of expressions is relevant
        """
        super().__init__()
        self._func = func
        self._expressions = tuple(map(possibly_parse_literal, expressions))
        self._commute = commute

    def get_expressions(self):
        """
        Gets a list of all the expressions of this Function
        TODO: deprecate this in favor of individual methods on subclasses

        Returns:
            The list of expressions of this Function
        """
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
        """
        Get the python function that acts on numeric values

        Returns:
            The function
        """
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
    """
    The sin operation
    """
    def __init__(self, expr):
        super().__init__(sin, expr)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import FunctionValueOnlySimplifier
        from expression.simplifier.TrigSimplifiers import SinAsinSimplifier
        return [SinAsinSimplifier(), FunctionValueOnlySimplifier()]

    def __repr__(self):
        return 'sin({})'.format(self._expressions[0].__repr__())


class Cos(Function):
    """
    The cos operation
    """
    def __init__(self, expr):
        super().__init__(cos, expr)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import FunctionValueOnlySimplifier
        from expression.simplifier.TrigSimplifiers import CosAcosSimplifier
        return [CosAcosSimplifier(), FunctionValueOnlySimplifier()]

    def __repr__(self):
        return 'cos({})'.format(self._expressions[0].__repr__())


class Asin(Function):
    """
    The asin operation
    """
    def __init__(self, expr):
        super().__init__(asin, expr)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import FunctionValueOnlySimplifier
        from expression.simplifier.TrigSimplifiers import AsinSinSimplifier
        return [AsinSinSimplifier(), FunctionValueOnlySimplifier()]

    def __repr__(self):
        return 'asin({})'.format(self._expressions[0].__repr__())


class Acos(Function):
    """
    The acos operation
    """
    def __init__(self, expr):
        super().__init__(acos, expr)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import FunctionValueOnlySimplifier
        from expression.simplifier.TrigSimplifiers import AcosCosSimplifier
        return [AcosCosSimplifier(), FunctionValueOnlySimplifier()]

    def __repr__(self):
        return 'acos({})'.format(self._expressions[0].__repr__())


class Negate(Function):
    """
    The negate operation
    """
    def __init__(self, expr):
        """
        Args:
            expr: The expression to be negated
        """
        super().__init__(lambda x: -x, expr)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import FunctionValueOnlySimplifier
        return [FunctionValueOnlySimplifier()]

    def __repr__(self):
        return '-{}'.format(self._expressions[0].__repr__())


class Add(Function):
    """
    The addition operation
    """
    def __init__(self, *expressions):
        """
        Args:
            *expressions: A list of expressions to be summed
        """
        super().__init__(lambda *x: sum(x), *expressions)
        if len(expressions) < 2:
            raise ValueError('Not enough expressions')

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import (
            FunctionValueOnlySimplifier,
        )
        from expression.simplifier.AddSimplifiers import (
            AddCombineTermsSimplifier,
            AddCombineValuesSimplifier,
            AddNestedAddSimplifier,
        )
        return [FunctionValueOnlySimplifier(),
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
    """
    The subtraction operation
    """
    def __init__(self, expr1, expr2):
        """
        Args:
            expr1: The expression to subtract from
            expr2: The expression to be subtracted
        """
        super().__init__(lambda a, b: a - b, expr1, expr2)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import FunctionValueOnlySimplifier
        from expression.simplifier.SubtractSimplifiers import SubtractWithZeroSimplifier
        return [FunctionValueOnlySimplifier(), SubtractWithZeroSimplifier()]

    def __repr__(self):
        return '({}-{})'.format(self._expressions[0].__repr__(), self._expressions[1].__repr__())


class Divide(Function):
    """
    The division operation
    """
    def __init__(self, numer, denom):
        """
        Args:
            numer: The numerator
            denom: The denominator
        """
        super().__init__(lambda a, b: a / b, numer, denom)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import FunctionValueOnlySimplifier
        from expression.simplifier.DivideSimplifiers import DivideByOneSimplifier
        return [FunctionValueOnlySimplifier(), DivideByOneSimplifier()]

    def __repr__(self):
        return '(({})/({}))'.format(self._expressions[0].__repr__(), self._expressions[1].__repr__())


class Multiply(Function):
    """
    The multiplication operation
    """
    def __init__(self, *expressions):
        """
        Args:
            *expressions: A list of the expressions to multiply together
        """
        super().__init__(lambda *l: reduce(lambda x, y: x * y, l), *expressions, commute=True)
        if len(expressions) < 2:
            raise ValueError('Not enough expressions')

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import (
            FunctionValueOnlySimplifier,
        )
        from expression.simplifier.MultiplySimplifiers import (
            MultiplyCombineValuesSimplifier,
            MultiplyCombineTermsSimplifier,
            MultiplyNestedMultiplySimplifier,
        )
        return [FunctionValueOnlySimplifier(),
                MultiplyNestedMultiplySimplifier(),
                MultiplyCombineValuesSimplifier(),
                MultiplyCombineTermsSimplifier(), ]

    def __repr__(self):
        return '(' + '*'.join(x.__repr__() for x in self.get_expressions()) + ')'


class Exponent(Function):
    """
    The exponentiation operation
    """
    def __init__(self, base, exponent):
        """
        Args:
            base: The base of the exponent
            exponent: The exponent
        """
        super().__init__(pow, base, exponent)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import FunctionValueOnlySimplifier
        from expression.simplifier.PowerSimplifiers import PowerOfZeroSimplifier
        from expression.simplifier.PowerSimplifiers import PowerOfOneSimplifier
        return [FunctionValueOnlySimplifier(), PowerOfOneSimplifier(), PowerOfZeroSimplifier()]

    def __repr__(self):
        exprs = self.get_expressions()
        return '({})^({})'.format(exprs[0], exprs[1])


class Log(Function):
    """
    The log operation
    """
    def __init__(self, n, base=e):
        """
        Args:
            n: The number to take the log of
            base: The base of the log
        """
        super().__init__(log, n, base)

    def get_simplifiers(self):
        from expression.simplifier.Simplifier import FunctionValueOnlySimplifier
        return [FunctionValueOnlySimplifier()]

    def __repr__(self):
        exprs = self.get_expressions()
        return 'Log(n={}, b={})'.format(exprs[0].__repr__(), exprs[1].__repr__())
