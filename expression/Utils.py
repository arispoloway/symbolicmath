
def reduce_all(l):
    return tuple(map(lambda x: x.simplify(), l))

def reduce_x(expr, n):
    new_expr = expr
    while n > 0:
        new_expr = new_expr.simplify()
        n -= 1
    return new_expr

def filter_split(func, l):
    good = []
    bad = []
    for x in l:
        if func(x):
            good.append(x)
        else:
            bad.append(x)
    return good, bad

