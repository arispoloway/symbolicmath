import logging
from abc import ABC, abstractmethod

logging.basicConfig()
log = logging.getLogger()


class Expression(ABC):
    """
    Represents a mathematical expression
    """
    def __init__(self):
        pass

    @abstractmethod
    def evaluate(self, **kwargs):
        """
        Evaluate this expression and attempt to return a Value

        Args:
            **kwargs: A mapping of variable names to numeric values to be substituted in, ex: {'x':3, 'y':4.5}
        Returns:
            A Value if the substitutions were sufficient, otherwise an Expression with Variables replaced
            by the appropriate Values, and reduced where possible
        """
        pass

    def get_numeric_value(self):
        """
        Gets the numeric value of a Value, None otherwise
        Returns:
            The numeric value of a Value, None if any other Expression
        """
        return None

    def get_simplifiers(self):
        """
        Gets a list of simplifiers known to potentially be able to act on this Expression
        Returns:
            The list
        """
        return []

    def simplify(self, whitelist=None):
        """
        Simplify this expression
        Args:
            whitelist: A whitelist of simplifiers to use
        Returns:
            A new expression that is the simplified form of this expression
        """
        return self

    def simplify_sub_expressions(self, whitelist=None):
        """
        Creates a new expression that is this expressions, with all sub expressions simplified
        Args:
            whitelist: A whitelist of simplifiers to use
        Returns:
            A new expression that is this expression with sub expressions simplified
        """
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




