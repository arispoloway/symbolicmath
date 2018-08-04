from expression.Variable import Variable

from expression.Value import Value


def isalpha(s):
    return all(c.isalpha() for c in s)


def possibly_parse_literal(x):
    if isinstance(x, (int, float)):
        return Value(x)
    if isinstance(x, str):
        return Variable(x)
    return x
