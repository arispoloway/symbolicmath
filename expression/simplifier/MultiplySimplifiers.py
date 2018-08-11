from collections import Counter
from functools import reduce
from itertools import chain

from expression.Function import Multiply, Add
from expression.Utils import filter_split
from expression.Value import Value
from expression.simplifier.Simplifier import Simplifier


class MultiplyNestedMultiplySimplifier(Simplifier):
    def can_simplify(self, expression):
        return isinstance(expression, Multiply) and \
               len([expr for expr in expression.get_expressions() if isinstance(expr, Multiply)]) != 0

    def _simplify(self, expression):
        mult, other = filter_split(lambda x: isinstance(x, Multiply), expression.get_expressions())
        mult = list(chain(*map(lambda x: x.get_expressions(), mult)))

        return Multiply(*mult, *other)


# TODO consider handling future case, where simplification may involve expanding powers,
# instead of combining into a power
# Will probably involve allowing specification of simplifiers, may be apt to rename transform with a heuristic to use
# ones that generally simplify

class MultiplyCombineTermsSimplifier(Simplifier):
    def can_simplify(self, expression):
        return isinstance(expression, Multiply)

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
        return isinstance(expression, Multiply) and len(
            [expr for expr in expression.get_expressions() if isinstance(expr, Value)]) > 0

    def _simplify(self, expression):
        values, other = filter_split(lambda x: isinstance(x, Value), expression.get_expressions())
        value = reduce(lambda x, y: x * y, map(lambda x: x.get_numeric_value(), values))

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


class MultiplyDistributionSimplifier(Simplifier):
    def can_simplify(self, expression):
        return isinstance(expression, Multiply) and any(isinstance(expr, Add) for expr in expression.get_expressions())

    def _simplify(self, expression):
        exprs = expression.get_expressions()

        add_term = None
        others = []

        for expr in exprs:
            if isinstance(expr, Add) and not add_term:
                add_term = expr
            else:
                others.append(expr)

        add_exprs = add_term.get_expressions()

        first_other = others[0]
        others = others[1:]

        if not others:
            return Add(*map(lambda x: first_other * x, add_exprs))
        return Multiply(*others, Add(*map(lambda x: first_other * x, add_exprs)))



