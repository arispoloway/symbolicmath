from expression.Expression import Expression
from abc import ABC, abstractmethod


class SimplifiableExpression(Expression, ABC):
    """
    An abstract class to represent an expression that is simplifiable
    """
    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def evaluate(self, **kwargs):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def get_simplifiers(self):
        pass

    def get_direct_transformations(self):
        simplifiers = self.get_simplifiers()
        return list(filter(lambda x: x != self, (s.simplify(self) for s in simplifiers)))
