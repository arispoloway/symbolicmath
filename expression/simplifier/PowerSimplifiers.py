from expression.Function import Exponent
from expression.Value import Value
from expression.simplifier.Simplifier import Simplifier


class PowerOfOneSimplifier(Simplifier):

    def can_simplify(self, expression):
        return isinstance(expression, Exponent) and expression.get_expressions()[1] == Value(1)

    def _simplify(self, expression):
        return expression.get_expressions()[0]


class PowerOfZeroSimplifier(Simplifier):

    def can_simplify(self, expression):
        return isinstance(expression, Exponent) and expression.get_expressions()[1] == Value(0)

    def _simplify(self, expression):
        return Value(1)


