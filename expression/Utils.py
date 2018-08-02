
def reduce_all(l):
    return tuple(map(lambda x: x.reduce(), l))

def reduce_x(expr, n):
    new_expr = expr
    while n > 0:
        new_expr = new_expr.reduce()
        n -= 1
    return new_expr