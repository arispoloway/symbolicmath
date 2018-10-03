from expression.Function import Sin, Asin, Cos
from expression.Variable import Variable
from collections import defaultdict
import heapq


def simplify(expr):
    previous = {}

    heap = []
    heapq.heappush(heap, (len(str(expr)), str(expr), expr))

    while len(heap) != 0:
        l, s, expr = heapq.heappop(heap)

        for new_expr in expr.get_transformations():
            if new_expr not in previous:
                previous[new_expr] = expr
                heapq.heappush(heap, (len(str(new_expr)), str(new_expr), new_expr))

    return previous


if __name__ == '__main__':
    x = Variable('x')
    expr = (Sin(x * 2) * (x + 1)) // x
    simp = simplify(expr)
    lens = [(e, len(str(e))) for e in simp.keys()]
    items = list(sorted(lens, key=lambda x: x[1]))
