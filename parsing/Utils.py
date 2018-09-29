from expression.Derivative import Derivative
from expression.Function import Sin, Asin, Cos, Acos, Log, Add, Subtract, Divide, Multiply, Exponent


def is_alpha(s):
    return all(c.isalpha() for c in s)


def parse_number(n):
    i = int(n)
    f = float(n)
    if i == f:
        return i
    return f


functions = {
    'sin':  (Sin, 1),
    'asin': (Asin, 1),
    'cos':  (Cos, 1),
    'acos': (Acos, 1),
    'log': (Log, 2),
}

operators = {
    '^': (4, 'r', Exponent),
    '*': (3, 'l', Multiply),
    '/': (3, 'l', Divide),
    '+': (2, 'l', Add),
    '-': (2, 'l', Subtract),
    '//': (1, 'l', Derivative),
}

# TODO combine function and operator? seem similar
# TODO handle negate vs subtract


def get_precedence(op):
    return operators.get(op, (None, None, None))[0]


def get_associativity(op):
    return operators.get(op, (None, None, None))[1]


def get_operator(op):
    return operators.get(op, (None, None, None))[2]


def is_operator(s):
    return s in operators


def is_function(s):
    return s in functions


def get_function(s):
    return functions.get(s.lower(), (None, None))[0]

def get_function_args(s):
    return functions.get(s.lower(), (None, None))[1]


def is_numeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Stack(object):
    def __init__(self):
        self._list = []

    def push(self, x):
        self._list.append(x)

    def pop(self):
        if len(self._list) > 0:
            return self._list.pop()
        raise IndexError()

    def peek(self):
        if len(self._list) > 0:
            return self._list[-1]
        raise IndexError()

    def is_empty(self):
        return len(self._list) == 0


class Queue(object):
    def __init__(self):
        self._list = []

    def push(self, x):
        self._list.append(x)

    def pop(self):
        if len(self._list) > 0:
            return self._list.pop(0)
        raise IndexError()

    def as_list(self):
        return self._list[::]

    def is_empty(self):
        return len(self._list) == 0


class Stream(object):
    def __init__(self, s):
        self._s = s
        self._pos = 0
        self._len = len(s)

    def peek(self, ahead=0):
        idx = self._pos + ahead
        if idx >= self._len:
            return None
        return self._s[self._pos + ahead]

    def take(self):
        self._pos += 1
        return self._s[self._pos - 1]

    def has_next(self):
        return self._pos < self._len