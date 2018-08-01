from Expression import Expression
from Function import Sin, Cos, Negate, Add, Subtract, Multiply
from Value import Value
from Variable import Variable


class Derivative(Expression):
    def __init__(self, expr, var):
        self._expr = expr
        self._var = var

    def get_expression(self):
        return self._expr

    def get_var(self):
        return self._var

    def evaluate(self, **kwargs):
        return Derivative(self._expr.evaluate(**kwargs), self._var)

    def reduce(self, **kwargs):
        if isinstance(self._expr, Value):
            return Value(0)
        if isinstance(self._expr, Variable):
            if self._expr.get_name() == self._var:
                return Value(1)
            return self
        if isinstance(self._expr, Sin):
            expr = self._expr.get_expressions()[0]
            return Derivative(expr, self._var) * Cos(expr)
        if isinstance(self._expr, Cos):
            expr = self._expr.get_expressions()[0]
            return Derivative(expr, self._var) * ( -Sin(expr))
        if isinstance(self._expr, Negate):
            expr = self._expr.get_expressions()[0]
            return -Derivative(expr, self._var)
        # TODO fux this with how ever many things to sum, also product
        if isinstance(self._expr, Add):
            exprs = self._expr.get_expressions()
            return Derivative(exprs[0], self._var) + Derivative(exprs[1], self._var)
        if isinstance(self._expr, Subtract):
            exprs = self._expr.get_expressions()
            return Derivative(exprs[0], self._var) - Derivative(exprs[1], self._var)
        if isinstance(self._expr, Multiply):
            exprs = self._expr.get_expressions()
            return exprs[1] * Derivative(exprs[0], self._var) +\
                   exprs[0] * Derivative(exprs[1], self._var)

    def __eq__(self, other):
        return isinstance(other, Derivative) and \
               self.get_expression() == other.get_expression() and \
               self.get_var() == other.get_var()

    def __repr__(self):
        return 'd({})/d{}'.format(self._expr, self._var)

