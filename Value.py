from Expression import Expression

class Value(Expression):
    def __init__(self, value):
        super().__init__()
        self._value = value

    def evaluate(self, **kwargs):
        return self

    def get_value(self):
        return self._value

    def __repr__(self):
        return '{}'.format(self._value)

