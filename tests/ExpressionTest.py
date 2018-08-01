import unittest

from Operation import Sin, Add
from Value import Value
from Variable import Variable


class VariableEvaluateTestCase(unittest.TestCase):
    def runTest(self):
        self.assertEqual(Variable('y').evaluate(y=3).get_value(), 3)

class SinEvaluateTestCase(unittest.TestCase):
    def runTest(self):
        self.assertAlmostEqual(Sin(Value(3)).evaluate().get_value(), 0.14112)

class AddEvaluateTestCase(unittest.TestCase):
    def runTest(self):
        self.assertEqual(Add(Value(3), Value(4)).evaluate().get_value(), 7)
        self.assertEqual(Add(Variable('x'), Value(4)).evaluate(x=3).get_value(), 7)

class AddSinEvaluateTestCase(unittest.TestCase):
    def runTest(self):
        self.assertAlmostEqual(Add(Sin(Value(3)), Value(4)).evaluate().get_value(), 4.14112)
        self.assertAlmostEqual(Add(Sin(Value(3)), Variable('y')).evaluate(y=4).get_value(), 4.14112)
        self.assertAlmostEqual(Add(Sin(Variable('x')), Variable('y')).evaluate(x=3, y=4).get_value(), 4.14112)

if __name__ == '__main__':
    unittest.main()


