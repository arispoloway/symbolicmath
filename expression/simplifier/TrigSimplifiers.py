from expression.Function import Sin, Asin, Cos, Acos
from expression.simplifier.Simplifier import Simplifier


class SinAsinSimplifier(Simplifier):
    def can_simplify(self, expression):
        return isinstance(expression, Sin) and isinstance(expression.get_expressions()[0], Asin)

    def _simplify(self, expression):
        return expression.get_expressions()[0].get_expressions()[0]


class AsinSinSimplifier(Simplifier):
    def can_simplify(self, expression):
        return isinstance(expression, Asin) and isinstance(expression.get_expressions()[0], Sin)

    def _simplify(self, expression):
        return expression.get_expressions()[0].get_expressions()[0]


class CosAcosSimplifier(Simplifier):
    def can_simplify(self, expression):
        return isinstance(expression, Cos) and isinstance(expression.get_expressions()[0], Acos)

    def _simplify(self, expression):
        return expression.get_expressions()[0].get_expressions()[0]


class AcosCosSimplifier(Simplifier):
    def can_simplify(self, expression):
        return isinstance(expression, Acos) and isinstance(expression.get_expressions()[0], Cos)

    def _simplify(self, expression):
        return expression.get_expressions()[0].get_expressions()[0]
