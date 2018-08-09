from expression.Variable import Variable
from expression.simplifier.DerivativeSimplifiers import *


from tests.utils import SimplifierTest


x, y, z = Variable('x'), Variable('y'), Variable('z')


class DeriveSinTestCase(SimplifierTest):
    simplifier = DerivativeSinSimplifier()

    def runTest(self):
        self.assertSimplify(Sin(x * 2) // x, ((x * 2) // x) * Cos(x * 2))


class DeriveCosTestCase(SimplifierTest):
    simplifier = DerivativeCosSimplifier()

    def runTest(self):
        self.assertSimplify(Cos(x * 2) // x, ((x * 2) // x) * - Sin(x * 2))


class DeriveNegateTestCase(SimplifierTest):
    simplifier = DerivativeNegateSimplifier()

    def runTest(self):
        self.assertSimplify((-(x + 3)) // x, -((x + 3) // x))


class DeriveAddTestCase(SimplifierTest):
    simplifier = DerivativeAddSimplifier()

    def runTest(self):
        self.assertSimplify((Sin(x) + x) // x, Sin(x) // x + x // x)


class DeriveSubtractTestCase(SimplifierTest):
    simplifier = DerivativeSubtractSimplifier()

    def runTest(self):
        self.assertSimplify((Sin(x) - x) // x, Sin(x) // x - x // x)


class DeriveDivideTestCase(SimplifierTest):
    simplifier = DerivativeDivideSimplifier()

    def runTest(self):
        self.assertSimplify((Sin(x) / x) // x, (x * (Sin(x) // x) - Sin(x) * (x // x)) / (x ^ 2))


class DeriveMultiplyTestCase(SimplifierTest):
    simplifier = DerivativeMultiplySimplifier()

    def runTest(self):
        self.assertSimplify((Sin(x) * x) // x, Sin(x) * (x // x) + x * (Sin(x) // x))
        # TODO write tests for multiplication with more terms


class DerivePowerTestCase(SimplifierTest):
    simplifier = DerivativeExponentSimplifier()

    def runTest(self):
        self.assertSimplify((x ^ 2) // x, Value(2) * (x ^ 1) * (x // x))


class DeriveExponentTestCase(SimplifierTest):
    simplifier = DerivativeExponentSimplifier()

    def runTest(self):
        self.assertSimplify((Value(2) ^ x) // x, Multiply(Value(2) ^ x, x // x, Log(2)))