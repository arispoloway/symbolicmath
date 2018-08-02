from expression.Expression import Expression

class Value(Expression):
    def __init__(self, value):
        super().__init__()
        if not isinstance(value, (int, float, complex)):
            raise ValueError('Invalid Value')
        self._value = value

    def evaluate(self, **kwargs):
        return self

    def get_value(self):
        return self._value

    def __eq__(self, other):
        return isinstance(other, Value) and \
               self.get_value() == other.get_value()

    def __hash__(self):
        return hash(self.get_value())

    def __repr__(self):
        return '{}'.format(self._value)
