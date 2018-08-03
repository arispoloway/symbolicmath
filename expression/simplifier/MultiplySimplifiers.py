from collections import Counter
from functools import reduce
from itertools import chain

from expression.Function import Multiply, Add
from expression.Utils import filter_split
from expression.Value import Value
from expression.simplifier.Simplifier import Simplifier


class MultiplyNestedMultiplySimplifier(Simplifier):

    def can_simplify(self, expression):
        return isinstance(expression, Multiply) and len([expr for expr in expression.get_expressions() if isinstance(expr, Multiply)]) != 0

    def _simplify(self, expression):
        mult, other = filter_split(lambda x: isinstance(x, Multiply), expression.get_expressions())
        mult = list(chain(*map(lambda x: x.get_expressions(), mult)))

        return Multiply(*mult, *other)


# TODO consider handling future case, where simplification may involve expanding powers, instead of combining into a power
# Will probably involve allowing specification of simplifiers, may be apt to rename transform with a heuristic to use
# ones that generally simplify

class MultiplyCombineTermsSimplifier(Simplifier):

    def can_simplify(self, expression):
        #TODO maybe rethink this can_simplify, seems to be kinda annoying to do here, somewhat duplicated
        # might just be better to do this check in simplify, and do nothing if not applicable
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
                exprs.append(term ^ Value(freq))

        if len(exprs) == 1:
            return exprs[0]
        return Multiply(*exprs)


class MultiplyCombineValuesSimplifier(Simplifier):

    def can_simplify(self, expression):
        return isinstance(expression, Multiply) and len([expr for expr in expression.get_expressions() if isinstance(expr, Value)]) > 0

    def _simplify(self, expression):
        values, other = filter_split(lambda x: isinstance(x, Value), expression.get_expressions())
        value = reduce(lambda x,y: x*y, map(lambda x: x.get_numeric_value(), values))

        if value == 0:
            return Value(0)
        if value == 1:
            if len(other) == 1:
                return other[0]
            return Multiply(*other)
        if value == -1:
            if len(other) == 1:
                return -other[0]
            return -Multiply(*other)
        return Multiply(value, *other)