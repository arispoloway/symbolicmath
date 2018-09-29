from expression.Value import Value
from expression.Variable import Variable


def simplify_all(l, whitelist=None):
    """
    Given a list of expressions, simplify each

    Args:
        l: The list of expressions
        whitelist: A whitelist of simplifiers to use
    Returns:
        The original list of expressions, simplified
    """
    return tuple(map(lambda x: x.simplify(whitelist=whitelist), l))


def filter_split(func, l):
    """
    Filter the given list based on a function, saving the filtered out values and returning both lists
    Args:
        func: The predicate to filter by
        l: The list of values
    Returns:
        Two lists, the first containing values for which the predicate returns True, the 2nd, False
    """
    good = []
    bad = []
    for x in l:
        if func(x):
            good.append(x)
        else:
            bad.append(x)
    return good, bad


def possibly_parse_literal(x):
    if isinstance(x, (int, float)):
        return Value(x)
    if isinstance(x, str):
        return Variable(x)
    return x