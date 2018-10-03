from expression.Derivative import Derivative
from expression.Function import Sin, Asin, Cos, Acos, Log, Add, Subtract, Divide, Multiply, Exponent


def is_alpha(s):
    """
    Is a string composed of entirely a-zA-Z
    :param s: The string
    :return: Whether or not it is exclusively a-zA-Z
    """
    return all(c.isalpha() for c in s)


def parse_number(n):
    """
    Parse a given number to the appropriate type
    :param n: The number as a string
    :return: A float or int version of the string
    """
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
    '^': (5, 'r', Exponent),
    '*': (4, 'l', Multiply),
    '/': (4, 'l', Divide),
    '+': (2, 'l', Add),
    '-': (2, 'l', Subtract),
    '//': (3, 'l', Derivative),
}

# TODO combine function and operator? seem similar
# TODO handle negate vs subtract


def get_precedence(op):
    """
    Get the precedence of the given operator, or None if it is not an operator
    :param op: The operator string
    :return: The operator precedence, or None
    """
    return operators.get(op, (None, None, None))[0]


def get_associativity(op):
    """
    Get the associativity of the given operator, or None if it is not an operator
    :param op: The operator string
    :return: The associativity, or None
    """
    return operators.get(op, (None, None, None))[1]


def get_operator(op):
    """
    Get the  of the given operator, or None if it is not an operator
    :param op: The operator string
    :return: The operator, or None
    """
    return operators.get(op, (None, None, None))[2]


def is_operator(s):
    """
    Is the given string an operator
    :param s: The string
    :return: Whether or not it is an operator
    """
    return s in operators


def is_function(s):
    """
    Is the given string a function
    :param s: The string
    :return: Whether or not it is a function
    """
    return s in functions


def get_function(s):
    """
    Get the function associated with the string, or None if it isn't a function
    :param s: The string
    :return: The associated function
    """
    return functions.get(s.lower(), (None, None))[0]


def get_function_args(s):
    """
    Get the number of arguments to the given function, or None if it isn't a function
    :param s: The string for the function
    :return: The argument count
    """
    return functions.get(s.lower(), (None, None))[1]


def is_numeric(s):
    """
    Is the given string a valid number
    :param s: The string
    :return: Whether or not it is a number
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


