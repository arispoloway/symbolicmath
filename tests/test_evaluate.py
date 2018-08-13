import unittest

from expression.Function import Sin, Add
from expression.Value import Value
from expression.Variable import Variable


class VariableEvaluateTestCase(unittest.TestCase):
    def runTest(self):
        self.assertEqual(Variable('y').evaluate(y=Value(3)).get_numeric_value(), 3)


class SinEvaluateTestCase(unittest.TestCase):
    def runTest(self):
        self.assertAlmostEqual(Sin(Value(3)).evaluate().get_numeric_value(), 0.14112)


class AddEvaluateTestCase(unittest.TestCase):
    def runTest(self):
        self.assertEqual(Add(Value(3), Value(4)).evaluate().get_numeric_value(), 7)
        self.assertEqual(Add(Variable('x'), Value(4)).evaluate(x=Value(3)).get_numeric_value(), 7)


class AddSinEvaluateTestCase(unittest.TestCase):
    def runTest(self):
        self.assertAlmostEqual(Add(Sin(Value(3)), Value(4)).evaluate().get_numeric_value(), 4.14112)
        self.assertAlmostEqual(Add(Sin(Value(3)), Variable('y')).evaluate(y=Value(4)).get_numeric_value(), 4.14112)
        self.assertAlmostEqual(Add(Sin(Variable('x')), Variable('y'))
                               .evaluate(x=Value(3), y=Value(4)).get_numeric_value(), 4.14112)