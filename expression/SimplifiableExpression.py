from expression.Expression import Expression
from abc import ABC, abstractmethod


class SimplifiableExpression(Expression, ABC):

    def simplify(self):
        current_expression = self
        past_expressions = set()
        change_this_iteration = True

        while change_this_iteration:
            change_this_iteration = False
            current_expression = current_expression.simplify_sub_expressions()
            simplifiers = current_expression.get_simplifiers()

            past_expressions.add(current_expression)
            for s in simplifiers:
                current_expression = s.simplify(current_expression)
                if current_expression not in past_expressions:
                    past_expressions.add(current_expression)
                    change_this_iteration = True


        return current_expression
