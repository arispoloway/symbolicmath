import logging
from abc import ABC, abstractmethod

logging.basicConfig()
log = logging.getLogger()


class Expression(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def evaluate(self, **kwargs):
        pass

    def get_numeric_value(self):
        return None

    def get_simplifiers(self):
        return []

    def simplify(self, whitelist=None):
        return self

    def simplify_sub_expressions(self, whitelist=None):
        return self

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    def __add__(self, other):
        import expression.Function
        # TODO maybe think more about this? Combining here seems logical for ease of use, especially while testing
        from expression.simplifier.AddSimplifiers import AddNestedAddSimplifier
        return AddNestedAddSimplifier().simplify(expression.Function.Add(self, other))

    def __mul__(self, other):
        import expression.Function
        from expression.simplifier.MultiplySimplifiers import MultiplyNestedMultiplySimplifier
        return MultiplyNestedMultiplySimplifier().simplify(expression.Function.Multiply(self, other))

    def __sub__(self, other):
        import expression.Function
        return expression.Function.Subtract(self, other)

    def __neg__(self):
        import expression.Function
        return expression.Function.Negate(self)

    def __truediv__(self, other):
        import expression.Function
        return expression.Function.Divide(self, other)

    def __floordiv__(self, other):
        import expression.Derivative
        return expression.Derivative.Derivative(self, other)

    def __xor__(self, other):
        import expression.Function
        return expression.Function.Exponent(self, other)




