from utils.data_structure_utils import Queue, Stack
from expression.Function import Sin, Asin, Cos
from expression.Variable import Variable
from expression.Value import Value
from collections import defaultdict


def simplify(expr):
    previous = {}

    queue = Queue()
    queue.push(expr)

    while not queue.is_empty():
        expr = queue.pop()

        transformations = expr.get_transformations()
        print(expr)
        print(len(transformations))
        if len(transformations) == 0:
            return expr
        for new_expr in transformations:
            if new_expr not in previous:
                previous[new_expr] = expr
                queue.push(new_expr)

    return previous

def simplify2(expr):
    blacklist = set()
    while True:
        ts = expr.get_transformations()
        n = next((e for e in ts if e not in blacklist), expr)
        if n == expr:
            return expr
        expr = n
        blacklist.add(expr)
        print(expr)


if __name__ == '__main__':
    x = Variable('x')
    expr = ((Value(2) * (x^2) + (Value(3) * Sin(x))) // x) * (x + 1)
    simp = simplify2(expr)
    print(simp)
