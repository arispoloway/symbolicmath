from expression.Function import Divide
from expression.Value import Value
from expression.simplifier.Simplifier import Simplifier


class DivideByOneSimplifier(Simplifier):
    def can_simplify(self, expression):
        return isinstance(expression, Divide) and expression.get_expressions()[1] in (Value(1), Value(-1))

    def _simplify(self, expression):
        numer, denom = expression.get_expressions()
        if denom == Value(1):
            return numer
        else:
            return -numer
