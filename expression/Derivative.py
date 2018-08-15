from expression.SimplifiableExpression import SimplifiableExpression
from expression.Value import Value
from parsing.Utils import possibly_parse_literal


class Derivative(SimplifiableExpression):
    def __init__(self, expr, var):
        super().__init__()
        self._expr = possibly_parse_literal(expr)
        self._var = possibly_parse_literal(var)
        if isinstance(self._var, Value):
            raise ValueError('Invalid respect to')

    def get_expression(self):
        return self._expr

    def get_var(self):
        return self._var

    def evaluate(self, **kwargs):
        return Derivative(self._expr.evaluate(**kwargs), self._var)

    # TODO rework this into a Function as well?
    def simplify_sub_expressions(self, whitelist=None):
        return Derivative(self._expr.simplify(whitelist=whitelist), self._var.simplify(whitelist=whitelist))

    def get_simplifiers(self):
        from expression.simplifier.DerivativeSimplifiers import (
            DerivativeConstantSimplifier,
            DerivativeVariableSimplifier,
            DerivativeSinSimplifier,
            DerivativeCosSimplifier,
            DerivativeNegateSimplifier,
            DerivativeAddSimplifier,
            DerivativeSubtractSimplifier,
            DerivativeMultiplySimplifier,
            DerivativeExponentSimplifier,
            DerivativeLogSimplifier,
            DerivativeDivideSimplifier,
        )

        return [
            DerivativeConstantSimplifier(),
            DerivativeVariableSimplifier(),
            DerivativeSinSimplifier(),
            DerivativeCosSimplifier(),
            DerivativeNegateSimplifier(),
            DerivativeAddSimplifier(),
            DerivativeSubtractSimplifier(),
            DerivativeMultiplySimplifier(),
            DerivativeExponentSimplifier(),
            DerivativeLogSimplifier(),
            DerivativeDivideSimplifier(),
        ]

    def __eq__(self, other):
        return isinstance(other, Derivative) and \
               self.get_expression() == other.get_expression() and \
               self.get_var() == other.get_var()

    def __hash__(self):
        return hash((type(self), self.get_expression(), self.get_var()))

    def __repr__(self):
        return 'd({})/d{}'.format(self._expr, self._var)

