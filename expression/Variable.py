from expression.Expression import Expression


class Variable(Expression):
    """
    An expression representing an unknown value
    """
    def __init__(self, name):
        """
        Args:
            name: Name to identify the variable by, ie 'x', 'y'
        """
        super().__init__()
        self._name = name

    def evaluate(self, **kwargs):
        if self._name in kwargs:
            from parsing.Utils import possibly_parse_literal
            return possibly_parse_literal(kwargs.get(self._name))
        return self

    def get_name(self):
        """
        Get the name of this variable

        Returns:
            The name of this variable
        """
        return self._name

    def __eq__(self, other):
        return isinstance(other, Variable) and \
               self.get_name() == other.get_name()

    def __hash__(self):
        return hash(self.get_name())

    def __repr__(self):
        return '{}'.format(self._name)

