from collections import Counter
from functools import reduce
from itertools import chain

from expression.Function import Multiply, Add
from expression.Value import Value
from expression.simplifier.Simplifier import Simplifier
from utils.expression_utils import filter_split


class MultiplyNestedMultiplySimplifier(Simplifier):
    def can_simplify(self, expression):
        return isinstance(expression, Multiply) and \
               len([expr for expr in expression.get_expressions() if isinstance(expr, Multiply)]) != 0

    def _simplify(self, expression):
        mult, other = filter_split(lambda x: isinstance(x, Multiply), expression.get_expressions())
        mult = list(chain(*map(lambda x: x.get_expressions(), mult)))

        return Multiply(*mult, *other)


class MultiplyDistributeSimplifier(Simplifier):
    def can_simplify(self, expression):
        return isinstance(expression, Multiply) and any(isinstance(x, Add) for x in expression.get_expressions())

    def _simplify(self, expression):
        exprs = list(expression.get_expressions())
        add = next(e for e in exprs if isinstance(e, Add))
        exprs.remove(add)
        terms = []
        for term in add.get_expressions():
            if len(exprs) == 1:
                terms.append(Multiply(exprs[0], term))
            else:
                terms.append(Multiply(Multiply(*exprs), term))
        return Add(*terms)


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
        if len(other) == 0:
            return Value(value)
        return Multiply(value, *other)

