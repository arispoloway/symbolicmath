import unittest

from expression.Function import *

from tests.utils import x, y, z

class AddCommutativeEqualityTestCase(unittest.TestCase):
    def runTest(self):
        self.assertEqual(x + y, y + x)
        self.assertEqual(Cos(x + y + z), Cos(z + y + x))
        self.assertEqual(Value(3) + Value(2), Value(2) + Value(3))


class MultiplyCommutativeEqualityTestCase(unittest.TestCase):
    def runTest(self):
        self.assertEqual(x * y, y * x)
        self.assertEqual(x * y * z, z * y * x)
        self.assertEqual(Cos(x * y * z), Cos(z * y * x))
        self.assertEqual(Value(3) * Value(2), Value(2) * Value(3))


class FunctionEqualityTestCase(unittest.TestCase):
    def assertSelfEquality(self, func, *args):
        self.assertEqual(func(*args), func(*args))

    def runTest(self):
        self.assertSelfEquality(Sin, x)
        self.assertSelfEquality(Cos, x)
        self.assertSelfEquality(Asin, x)
        self.assertSelfEquality(Acos, x)
        self.assertSelfEquality(Negate, x)
        self.assertSelfEquality(Add, x, y)
        self.assertSelfEquality(Subtract, x, y)
        self.assertSelfEquality(Divide, x, y)
        self.assertSelfEquality(Multiply, x, y)
        self.assertSelfEquality(Exponent, x, y)
        self.assertSelfEquality(Log, x, y)


