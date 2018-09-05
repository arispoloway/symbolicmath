from expression.Expression import Expression


class Value(Expression):
    """
    An expression representing a literal numeric value
    """
    def __init__(self, value):
        """
        Args:
            value: The value
        """
        super().__init__()
        if not isinstance(value, (int, float, complex)):
            raise ValueError('Invalid Value')
        self._value = value

    def evaluate(self, **kwargs):
        return self

    def get_numeric_value(self):
        return self._value

    def __eq__(self, other):
        return isinstance(other, Value) and \
               self.get_numeric_value() == other.get_numeric_value()

    def __hash__(self):
        return hash(self.get_numeric_value())

    def __repr__(self):
        return '{}'.format(self._value)
