def simplify_all(l):
    return tuple(map(lambda x: x.simplify(), l))


def filter_split(func, l):
    good = []
    bad = []
    for x in l:
        if func(x):
            good.append(x)
        else:
            bad.append(x)
    return good, bad
