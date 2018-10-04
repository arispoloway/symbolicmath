from collections import Counter
from functools import reduce
from itertools import chain

from expression.Function import Add, Multiply
from expression.Value import Value
from expression.simplifier.Simplifier import Simplifier
from utils.expression_utils import filter_split


class AddNestedAddSimplifier(Simplifier):
    def can_simplify(self, expression):
        return isinstance(expression, Add) and \
               len([expr for expr in expression.get_expressions() if isinstance(expr, Add)]) != 0

    def _simplify(self, expression):
        adds, other = filter_split(lambda x: isinstance(x, Add), expression.get_expressions())
        adds = list(chain(*map(lambda x: x.get_expressions(), adds)))

        return Add(*adds, *other)


class AddCombineValuesSimplifier(Simplifier):
    def can_simplify(self, expression):
        return isinstance(expression, Add) and \
               len([expr for expr in expression.get_expressions() if isinstance(expr, Value)]) > 0

    def _simplify(self, expression):
        values, other = filter_split(lambda x: isinstance(x, Value), expression.get_expressions())
        value = reduce(lambda x, y: x + y, map(lambda x: x.get_numeric_value(), values))

        if len(other) == 0:
            return Value(value)
        if value == 0:
            if len(other) == 1:
                return other[0]
            return Add(*other)
        return Add(value, *other)


class AddCombineTermsSimplifier(Simplifier):
    def can_simplify(self, expression):
        return isinstance(expression, Add)

    def _simplify(self, expression):
        exprs = expression.get_expressions()
        counts = Counter(exprs)
        exprs = []
        for term in counts:
            freq = counts[term]
            if freq == 1:
                exprs.append(term)
            else:
                exprs.append(Value(freq) * term)

        if len(exprs) == 1:
            return exprs[0]
        return Add(*exprs)

class AddFactorSimplifier(Simplifier):
    def can_simplify(self, expression):

        return isinstance(expression, Add) and \
               len([x for x in expression.get_expressions() if isinstance(x, Multiply)]) > 1

    def _simplify(self, expression):

        multiplies, others = filter_split(lambda x: isinstance(x, Multiply), expression.get_expressions())

        sets = [set(x.get_expressions()) for x in multiplies]
        c = Counter()
        for s in sets:
            c.update(s)
        term, count = c.most_common(1)[0]

        if count < 2:
            return expression

        in_terms = []

        for mult in multiplies:
            if term in mult.get_expressions():
                l = list(mult.get_expressions())
                l.remove(term)
                if len(l) == 1:
                    in_terms.append(l[0])
                else:
                    in_terms.append(Multiply(*l))
            else:
                others.append(mult)

        if len(others) == 0:
            return term * Add(*in_terms)
        return Add(term * Add(*in_terms), *others)







