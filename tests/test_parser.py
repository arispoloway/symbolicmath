import unittest

from parsing.Tokenizer import tokenize
from parsing.Parser import parse_to_expression, shunting_yard

from expression.Value import Value
from expression.Variable import Variable
from expression.Function import Sin, Log
from expression.Derivative import Derivative


class ParserTest(unittest.TestCase):

    def assertParsed(self, s, exp):
        self.assertEquals(parse_to_expression(s), exp)


class OrderOfOperationsTest(ParserTest):
    def runTest(self):
        self.assertParsed("5 * 3 + 3", (Value(5) * Value(3)) + Value(3))
        self.assertParsed("5 * 3 ^ 5 + 3", (Value(5) * (Value(3) ^ Value(5))) + Value(3))


class VariableTest(ParserTest):
    def runTest(self):
        self.assertParsed("5 * x", Value(5) * Variable('x'))


class FunctionTest(ParserTest):
    def runTest(self):
        self.assertParsed("5 * sin(x)", Value(5) * Sin(Variable('x')))
        self.assertParsed("5 * log(2, x)", Value(5) * Log(2, Variable('x')))


class DerivativeTest(ParserTest):
    def runTest(self):
        self.assertParsed("5 // x", Derivative(Value(5), Variable('x')))
        self.assertParsed("sin(x) // x", Derivative(Sin('x'), Variable('x')))


class ShuntingYardTest(unittest.TestCase):
    def assertParsed(self, s, q):
        self.assertEquals(shunting_yard(tokenize(s)).as_list(), q.split())


class ShuntingOrderOperationsTest(ShuntingYardTest):
    def runTest(self):
        self.assertParsed('3 * 4', '3 4 *')
        self.assertParsed('3 // x + 3', '3 x // 3 +')
        self.assertParsed('3 * 4 + 3', '3 4 * 3 +')
        self.assertParsed('3 * 4 + 3 ^ 2', '3 4 * 3 2 ^ +')
        self.assertParsed('3 * 4 ^ 5 + 3 ^ 2', '3 4 5 ^ * 3 2 ^ +')


class ShuntingFunctionTest(ShuntingYardTest):
    def runTest(self):
        self.assertParsed('3 * sin(4)', '3 4 sin *')
        self.assertParsed('3 * sin(4 + 3)', '3 4 3 + sin *')


class ShuntingParentheses(ShuntingYardTest):
    def runTest(self):
        self.assertParsed('2 * (4 + 3)', '2 4 3 + *')
        self.assertParsed('(3 * 2) + 4', '3 2 * 4 +')
