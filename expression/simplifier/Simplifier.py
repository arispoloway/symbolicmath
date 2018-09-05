from abc import ABC, abstractmethod

from expression.Function import Function
from expression.Value import Value


class Simplifier(ABC):
    """
    Represents an action that changes an expression to an equivalent form
    """
    @abstractmethod
    def can_simplify(self, expression):
        """
        Determine if this simplifier can simplify a given expression

        Args:
            expression: The expression to potentially be acted upon
        Returns:
            A boolean representing whether or not this simplifier can act on a given expression
        """
        pass

    @abstractmethod
    def _simplify(self, expression):
        """
        Simplify a given expression, assuming that it is already capable of being simplified by this simplifier

        Args:
            expression: The expression to simplify
        Returns:
            The simplified expression
        """
        pass

    def simplify(self, expression):
        """
        Simplifies a given expression, assuming it can be simplified, otherwise returns the input

        Args:
            expression: The expression to simplify
        Returns:
            The simplified expression, or the original if simplification is not possible
        """
        if self.can_simplify(expression):
            return self._simplify(expression)
        return expression


class FunctionValueOnlySimplifier(Simplifier):
    """
    A simplifier that simplifies Functions where all sub expressions are Values
    """
    def can_simplify(self, expression):
        return isinstance(expression, Function) and all(isinstance(e, Value) for e in expression.get_expressions())

    def _simplify(self, expression):
        return Value(expression.get_func()(*(e.get_numeric_value() for e in expression.get_expressions())))

# TODO write Exponent and Log simplifiers
