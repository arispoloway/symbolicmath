from Expression import Expression
from Value import Value

class Variable(Expression):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def evaluate(self, **kwargs):
        if self._name in kwargs:
            return Value(kwargs.get(self._name))

    def get_name(self):
        return self._name

    def __repr__(self):
        return '{}'.format(self._name)

