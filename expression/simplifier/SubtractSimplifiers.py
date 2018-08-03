from expression.Function import Subtract
from expression.Value import Value
from expression.simplifier.Simplifier import Simplifier


class SubtractWithZeroSimplifier(Simplifier):

    def can_simplify(self, expression):
        return isinstance(expression, Subtract) and any(x==Value(0) for x in expression.get_expressions())

    def _simplify(self, expression):
        first, second = expression.get_expressions()
        if first == Value(0):
            return -second
        else:
            return first