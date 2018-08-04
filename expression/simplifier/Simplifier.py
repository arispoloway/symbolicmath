from abc import ABC, abstractmethod

from expression.Function import Function
from expression.Value import Value


class Simplifier(ABC):
    @abstractmethod
    def can_simplify(self, expression):
        pass

    @abstractmethod
    def _simplify(self, expression):
        pass

    def simplify(self, expression):
        if self.can_simplify(expression):
            return self._simplify(expression)
        return expression


class ValueOnlySimplifier(Simplifier):
    def can_simplify(self, expression):
        return isinstance(expression, Function) and all(isinstance(e, Value) for e in expression.get_expressions())

    def _simplify(self, expression):
        return Value(expression.get_func()(*(e.get_numeric_value() for e in expression.get_expressions())))

# TODO write Derivative, Exponent and Log simplifiers
