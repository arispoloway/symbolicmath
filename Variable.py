from Expression import Expression
from Value import Value

class Variable(Expression):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def evaluate(self, **kwargs):
        if self._name in kwargs:
            return kwargs.get(self._name)
        return self

    def get_name(self):
        return self._name

    def __eq__(self, other):
        return isinstance(other, Variable) and \
               self.get_name() == other.get_name()

    def __hash__(self):
        return hash(self.get_name())

    def __repr__(self):
        return '{}'.format(self._name)

