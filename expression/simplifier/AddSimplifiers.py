from collections import Counter
from functools import reduce
from itertools import chain

from expression.Function import Add
from expression.Utils import filter_split
from expression.Value import Value
from expression.simplifier.Simplifier import Simplifier


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
