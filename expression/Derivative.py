from expression.SimplifiableExpression import SimplifiableExpression
from expression.Value import Value
from utils.expression_utils import possibly_parse_literal


class Derivative(SimplifiableExpression):
    """
    Represents a derivative operation
    """
    def __init__(self, expr, var):
        """
        Args:
            expr: The expression to take the derivative of
            var: The variable (or expression) to take with respect to
        """
        super().__init__()
        self._expr = possibly_parse_literal(expr)
        self._var = possibly_parse_literal(var)
        if isinstance(self._var, Value):
            raise ValueError('Invalid respect to')

    def get_expression(self):
        """
        Gets the expression
        Returns:
            The expression
        """
        return self._expr

    def get_var(self):
        """
        Gets the variable (or expression) this derivative is respect to
        Returns:
            The variable
        """
        return self._var

    def evaluate(self, **kwargs):
        # TODO maybe rethink evaluation / simplifying here? this seems to work but questionable
        simplified = self.simplify()
        if simplified == self:
            return self
        return simplified.evaluate(**kwargs)

    def get_transformations(self):
        direct = self.get_direct_transformations()
        sub_transformations = []
        expr_transformations = self.get_expression().get_transformations()
        var_transformations = self.get_var().get_transformations()
        for transformation in expr_transformations:
            sub_transformations.append(Derivative(transformation, self.get_var()))
        for transformation in var_transformations:
            sub_transformations.append(Derivative(self.get_expression(), transformation))
        return direct + sub_transformations

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

