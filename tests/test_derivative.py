import unittest

from expression.Function import *
from expression.Variable import Variable
from expression.Value import Value
from expression.Utils import reduce_x

from expression.Derivative import Derivative


# TODO rework all simplifier tests like those in test_simplifier, total simplifications to test_simplify
class DeriveSinTestCase(unittest.TestCase):
    def runTest(self):
        expr = Derivative(Sin('x') - 1, 'x').simplify()
        self.assertEqual(expr, Cos('x'))
        expr = Derivative(Sin(Value(2) * 'x') - 1, 'x').simplify()
        self.assertEqual(expr, Value(2) * Cos(Value(2) * 'x'))


class DeriveCosTestCase(unittest.TestCase):
    def runTest(self):
        expr = Derivative(Cos('x') - 1, 'x').simplify()
        self.assertEqual(expr, -Sin('x'))
        expr = Derivative(Cos(Value(2) * 'x') - 1, 'x').simplify()
        self.assertEqual(expr, Value(2) * (-Sin(Value(2) * 'x')))


class DeriveNegateTestCase(unittest.TestCase):
    def runTest(self):
        expr = Derivative(-Variable('x') - 1, 'x').simplify()
        self.assertEqual(expr, Value(-1))


class DeriveAddTestCase(unittest.TestCase):
    def runTest(self):
        expr = Derivative(Sin('x') + Variable('x') + 1 + 8, 'x').simplify()
        self.assertEqual(expr, Cos('x') + 1)


class DeriveSubtractTestCase(unittest.TestCase):
    def runTest(self):
        expr = Derivative(Sin('x') - Variable('x'), 'x').simplify()
        self.assertEqual(expr, Cos('x') - 1)


class DeriveDivideTestCase(unittest.TestCase):
    def runTest(self):
        expr = reduce_x(Derivative(Sin('x') / Variable('x'), 'x'), 2)
        self.assertEqual(expr, (Cos('x') * 'x' - Sin('x')) / (Variable('x') ^ 2))


class DeriveMultiplyTestCase(unittest.TestCase):
    def runTest(self):
        expr = reduce_x(Derivative(Sin('x') * Variable('x'), 'x'), 2)
        self.assertEqual(expr, Sin('x') + Variable('x') * Cos('x'))
        # TODO write tests for multiplication with more terms


class DerivePowerTestCase(unittest.TestCase):
    def runTest(self):
        expr = reduce_x(Derivative(Variable('x') ^ 2, 'x'), 2)
        self.assertEqual(expr, Value(2) * 'x')
        expr = reduce_x(Derivative((Variable('x') * 2) ^ 2, 'x'), 2)
        self.assertEqual(expr, Value(8) * 'x')
