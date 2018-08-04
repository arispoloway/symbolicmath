import unittest
from expression.simplifier.AddSimplifiers import *
from expression.simplifier.DerivativeSimplifiers import *
from expression.simplifier.DivideSimplifiers import *
from expression.simplifier.MultiplySimplifiers import *
from expression.simplifier.PowerSimplifiers import *
from expression.simplifier.SubtractSimplifiers import *
from expression.simplifier.TrigSimplifiers import *

from expression.Function import Sin, Add, Multiply, Asin, Cos, Acos
from expression.Variable import Variable

from expression.Value import Value

from tests.utils import SimplifierTest

x = Variable('x')
y = Variable('y')
z = Variable('z')


class DivideByOneTest(SimplifierTest):
    simplifier = DivideByOneSimplifier()

    def runTest(self):
        self.assertSimplify(x / 1, x)


class MultiplyNestedSimplifierTest(SimplifierTest):
    simplifier = MultiplyNestedMultiplySimplifier()

    def runTest(self):
        self.assertSimplify((x * y) * z, Multiply(x, y, z))


class MultiplyCombineTermsSimplifierTest(SimplifierTest):
    simplifier = MultiplyCombineTermsSimplifier()

    def runTest(self):
        self.assertSimplify(x * x, x ^ 2)
        self.assertSimplify(Multiply(x, y, x), (x ^ 2) * y)


class MultiplyCombineValuesSimplifierTest(SimplifierTest):
    simplifier = MultiplyCombineValuesSimplifier()

    def runTest(self):
        self.assertSimplify(Multiply(3, 4, x), Multiply(12, x))
        self.assertSimplify(Multiply(3, 4, x - 1), Multiply(12, x - 1))


class PowerOfOneSimplifierTest(SimplifierTest):
    simplifier = PowerOfOneSimplifier()

    def runTest(self):
        self.assertSimplify(x ^ 1, x)
        self.assertSimplify((x + y) ^ 1, x + y)


class PowerOfZeroSimplifierTest(SimplifierTest):
    simplifier = PowerOfZeroSimplifier()

    def runTest(self):
        self.assertSimplify(x ^ 0, Value(1))
        self.assertSimplify((x + y) ^ 0, Value(1))


class SubtractZeroSimplifierTest(SimplifierTest):
    simplifier = SubtractWithZeroSimplifier()

    def runTest(self):
        self.assertSimplify(x - 0, x)
        self.assertSimplify((x + y) - 0, x + y)


class SinAsinSimplifierTest(SimplifierTest):
    simplifier = SinAsinSimplifier()

    def runTest(self):
        self.assertSimplify(Sin(Asin(x - 1)), x - 1)


class AsinSinSimplifierTest(SimplifierTest):
    simplifier = AsinSinSimplifier()

    def runTest(self):
        self.assertSimplify(Asin(Sin(x - 1)), x - 1)


class CosAcosSimplifierTest(SimplifierTest):
    simplifier = CosAcosSimplifier()

    def runTest(self):
        self.assertSimplify(Cos(Acos(x - 1)), x - 1)


class AcosCosSimplifierTest(SimplifierTest):
    simplifier = AcosCosSimplifier()

    def runTest(self):
        self.assertSimplify(Acos(Cos(x - 1)), x - 1)


class AddNestedAddSimplifier(SimplifierTest):
    simplifier = AddNestedAddSimplifier()

    def runTest(self):
        self.assertSimplify((x + y) + z, Add(z, y, x))


class AddCombineValuesSimplifier(SimplifierTest):
    simplifier = AddCombineValuesSimplifier()

    def runTest(self):
        self.assertSimplify(Add(x, 3, 5), Add(x, 8))
        self.assertSimplify(Add(x - 1, 3, 5), Add(x - 1, 8))


class AddCombineTermsSimplifier(SimplifierTest):
    simplifier = AddCombineTermsSimplifier()

    def runTest(self):
        self.assertSimplify(x + x, x * 2)
