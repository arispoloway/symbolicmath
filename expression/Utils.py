def simplify_all(l, whitelist=None):
    return tuple(map(lambda x: x.simplify(whitelist=whitelist), l))


def filter_split(func, l):
    good = []
    bad = []
    for x in l:
        if func(x):
            good.append(x)
        else:
            bad.append(x)
    return good, bad
