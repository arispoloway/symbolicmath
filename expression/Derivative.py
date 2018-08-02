from functools import reduce

from expression.Expression import Expression
from expression.Function import Sin, Cos, Negate, Add, Subtract, Multiply
from expression.Value import Value
from parsing.Utils import possibly_parse_literal


class Derivative(Expression):
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

    def reduce(self, **kwargs):
        expr = self._expr.reduce()
        var = self._var.reduce()
        if isinstance(expr, Value):
            return Value(0)
        if expr == var:
            return Value(1)
        if isinstance(expr, Sin):
            expr = expr.get_expressions()[0]
            return (Derivative(expr.reduce(), var) * Cos(expr.reduce())).reduce()
        if isinstance(expr, Cos):
            expr = expr.get_expressions()[0]
            return (Derivative(expr.reduce(), var) * (-Sin(expr.reduce()))).reduce()
        if isinstance(expr, Negate):
            expr = expr.get_expressions()[0]
            return -(Derivative(expr.reduce(), var)).reduce()
        # TODO fix this with how ever many things to sum, also product
        if isinstance(expr, Add):
            exprs = expr.get_expressions()
            return reduce(lambda x, y:
                          Derivative(x.reduce(), var).reduce() +
                          Derivative(y.reduce(), var).reduce(), exprs)
        if isinstance(expr, Subtract):
            exprs = expr.get_expressions()
            return Derivative(exprs[0].reduce(), var).reduce() - \
                   Derivative(exprs[1].reduce(), var).reduce()
        if isinstance(expr, Multiply):
            exprs = expr.get_expressions()
            return exprs[1] * Derivative(exprs[0], var) +\
                   exprs[0] * Derivative(exprs[1], var)

    def __eq__(self, other):
        return isinstance(other, Derivative) and \
               self.get_expression() == other.get_expression() and \
               self.get_var() == other.get_var()

    def __repr__(self):
        return 'd({})/d{}'.format(self._expr, self._var)

