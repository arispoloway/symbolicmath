from expression.simplifier.AddSimplifiers import *
from expression.simplifier.DivideSimplifiers import *
from expression.simplifier.MultiplySimplifiers import *
from expression.simplifier.PowerSimplifiers import *
from expression.simplifier.SubtractSimplifiers import *
from expression.simplifier.TrigSimplifiers import *

from expression.Function import Sin, Add, Multiply, Asin, Cos, Acos

from expression.Value import Value

from tests.utils import SimplifierTest, x, y, z


# TODO test errors

class DivideByOneTest(SimplifierTest):
    simplifier = DivideByOneSimplifier()

    def runTest(self):
        self.assertSimplify(x / 1, x)


class MultiplyNestedSimplifierTest(SimplifierTest):
    simplifier = MultiplyNestedMultiplySimplifier()

    def runTest(self):
        self.assertSimplify((x * y) * z, Multiply(x, y, z))


class MultiplyDistributeSimplifierTest(SimplifierTest):
    simplifier = MultiplyDistributeSimplifier()

    def runTest(self):
        self.assertSimplify(x * (x + x), (x * x) + (x * x))
        self.assertSimplify(x * (x + x + x), (x * x) + (x * x) + (x * x))
        self.assertSimplify(Multiply(x, y, (x + 1)), Multiply((x * y), x) + Multiply((x * y), 1))


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


class AddNestedAddSimplifierTest(SimplifierTest):
    simplifier = AddNestedAddSimplifier()

    def runTest(self):
        self.assertSimplify((x + y) + z, Add(z, y, x))


class AddCombineValuesSimplifierTest(SimplifierTest):
    simplifier = AddCombineValuesSimplifier()

    def runTest(self):
        self.assertSimplify(Add(x, 3, 5), Add(x, 8))
        self.assertSimplify(Add(x - 1, 3, 5), Add(x - 1, 8))


class AddCombineTermsSimplifierTest(SimplifierTest):
    simplifier = AddCombineTermsSimplifier()

    def runTest(self):
        self.assertSimplify(x + x, x * 2)
        self.assertSimplify(x + x + x, x * 3)
        self.assertSimplify(x + 4 + x + x, x * 3 + 4)


class AddFactorSimplifierTest(SimplifierTest):
    simplifier = AddFactorSimplifier()

    def runTest(self):
        self.assertSimplify((x * 2) + (x * x), x * (x + 2))
        self.assertSimplify((Cos(x) * 2) + (Cos(x) * x), Cos(x) * (x + 2))
        self.assertSimplify((x * 2) + (x * x) + (x * y), x * (x + 2 + y))
        self.assertSimplify((x * 2) + (y * 3), (x * 2) + (y * 3))

