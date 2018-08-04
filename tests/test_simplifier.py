import unittest
from expression.Function import Sin, Add, Multiply, Asin, Cos, Acos
from expression.Variable import Variable

from expression.Value import Value

x = Variable('x')
y = Variable('y')
z = Variable('z')


class DivideByOneTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual((x / 1).simplify(), Variable('x'))


class MultiplyNestedSimplifierTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual(((x * y) * z).simplify(), Multiply(x, y, z))


class MultiplyCombineTermsSimplifierTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual(((x * y) * z).simplify(), Multiply(y, x, z))


class MultiplyCombineValuesSimplifierTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual(((x * 3) * 4).simplify(), Multiply(12, x))
        self.assertEqual(((x * 3) * (Value(4) * 4)).simplify(), Multiply(48, x))
        self.assertEqual(((x * 0) * (Value(4) * 4)).simplify(), Value(0))


class PowerOfOneSimplifierTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual((x ^ 1).simplify(), x)
        self.assertEqual(((x + y) ^ 1).simplify(), x + y)


class PowerOfZeroSimplifierTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual((x ^ 0).simplify(), Value(1))
        self.assertEqual(((x + y) ^ 0).simplify(), Value(1))


class SubtractZeroSimplifierTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual((x - 0).simplify(), x)
        self.assertEqual(((x + y) - 0).simplify(), x + y)


class SinAsinSimplifierTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual(Sin(Asin(x - 1)).simplify(), x - 1)


class AsinSinSimplifierTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual(Asin(Sin(x - 1)).simplify(), x - 1)


class CosAcosSimplifierTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual(Cos(Acos(x - 1)).simplify(), x - 1)


class AcosCosSimplifierTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual(Acos(Cos(x - 1)).simplify(), x - 1)


class AddNestedAddSimplifier(unittest.TestCase):
    def runTest(self):
        self.assertEqual(((x + y) + z).simplify(), Add(z, y, x))


class AddCombineValuesSimplifier(unittest.TestCase):
    def runTest(self):
        self.assertEqual(((x + 3) + 5).simplify(), Add(x, 8))
        self.assertEqual(((x + 3) + (5 + 1 + 3)).simplify(), Add(12, x))


class AddCombineTermsSimplifier(unittest.TestCase):
    def runTest(self):
        self.assertEqual((x + x).simplify(), x * 2)
        # TODO currently failing, will require possibly another simplifier? Gets tricky here
        self.assertEqual(((x + x) + (x + 1 + 3)).simplify(), Add(4, x * 3))
