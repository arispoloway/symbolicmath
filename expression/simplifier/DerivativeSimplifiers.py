from expression.Derivative import Derivative
from expression.Function import Sin, Cos, Negate, Add, Subtract, Multiply, Exponent, Log, Power, Divide
from expression.Value import Value
from expression.simplifier.Simplifier import Simplifier
from abc import ABC, abstractmethod


class DerivativeSimplifier(Simplifier, ABC):
    @abstractmethod
    def can_simplify(self, expression):
        pass

    @staticmethod
    def valid_if_type(e, t):
        return isinstance(e, Derivative) and isinstance(e.get_expression(), t)


class DerivativeConstantSimplifier(DerivativeSimplifier):
    def can_simplify(self, expression):
        return DerivativeSimplifier.valid_if_type(expression, Value)

    def _simplify(self, expression):
        return Value(0)


class DerivativeVariableSimplifier(DerivativeSimplifier):
    def can_simplify(self, expression):
        return isinstance(expression, Derivative) and expression.get_var() == expression.get_expression()

    def _simplify(self, expression):
        return Value(1)


class DerivativeSinSimplifier(DerivativeSimplifier):
    def can_simplify(self, expression):
        return DerivativeSimplifier.valid_if_type(expression, Sin)

    def _simplify(self, expression):
        expr = expression.get_expression()
        var = expression.get_var()
        return Derivative(expr.get_expressions()[0], var) * Cos(expr.get_expressions()[0])


class DerivativeCosSimplifier(DerivativeSimplifier):
    def can_simplify(self, expression):
        return DerivativeSimplifier.valid_if_type(expression, Cos)

    def _simplify(self, expression):
        expr = expression.get_expression()
        var = expression.get_var()
        return Derivative(expr.get_expressions()[0], var) * (-Sin(expr.get_expressions()[0]))


class DerivativeNegateSimplifier(DerivativeSimplifier):
    def can_simplify(self, expression):
        return DerivativeSimplifier.valid_if_type(expression, Negate)

    def _simplify(self, expression):
        expr = expression.get_expression()
        var = expression.get_var()
        return -(Derivative(expr.get_expressions()[0], var))


class DerivativeAddSimplifier(DerivativeSimplifier):
    def can_simplify(self, expression):
        return DerivativeSimplifier.valid_if_type(expression, Add)

    def _simplify(self, expression):
        expr = expression.get_expression()
        var = expression.get_var()
        exprs = expr.get_expressions()
        return Add(*map(lambda x: Derivative(x, var), exprs))


class DerivativeSubtractSimplifier(DerivativeSimplifier):
    def can_simplify(self, expression):
        return DerivativeSimplifier.valid_if_type(expression, Subtract)

    def _simplify(self, expression):
        expr = expression.get_expression()
        var = expression.get_var()
        exprs = expr.get_expressions()
        return Derivative(exprs[0], var) - Derivative(exprs[1], var)


# Todo fix this for more than 2 terms
class DerivativeMultiplySimplifier(DerivativeSimplifier):
    def can_simplify(self, expression):
        return DerivativeSimplifier.valid_if_type(expression, Multiply)

    def _simplify(self, expression):
        expr = expression.get_expression()
        var = expression.get_var()
        exprs = expr.get_expressions()
        first_two = exprs[1] * Derivative(exprs[0], var) + exprs[0] * Derivative(exprs[1], var)
        return first_two


class DerivativeExponentSimplifier(DerivativeSimplifier):
    def can_simplify(self, expression):
        return DerivativeSimplifier.valid_if_type(expression, Exponent)

    def _simplify(self, expression):
        expr = expression.get_expression()
        var = expression.get_var()
        base, exp = expr.get_expressions()
        return (expr * Log(base)) * (exp // var)


class DerivativeLogSimplifier(DerivativeSimplifier):
    def can_simplify(self, expression):
        return DerivativeSimplifier.valid_if_type(expression, Log)

    def _simplify(self, expression):
        expr = expression.get_expression()
        var = expression.get_var()
        exprs = expr.get_expressions()
        return Divide(Value(1), Log(exprs[1]) * exprs[0]) * (exprs[0] // var)


class DerivativePowerSimplifier(DerivativeSimplifier):
    def can_simplify(self, expression):
        return DerivativeSimplifier.valid_if_type(expression, Power)

    def _simplify(self, expression):
        expr = expression.get_expression()
        var = expression.get_var()
        base, exp = expr.get_expressions()
        return exp * (base ^ (exp - 1).simplify()) * (base // var)


class DerivativeDivideSimplifier(DerivativeSimplifier):
    def can_simplify(self, expression):
        return DerivativeSimplifier.valid_if_type(expression, Divide)

    def _simplify(self, expression):
        expr = expression.get_expression()
        var = expression.get_var()
        num, den = expr.get_expressions()
        return Divide(((num // var) * den) - (num * (den // var)), den ^ 2)
