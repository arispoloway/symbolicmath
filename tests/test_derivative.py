from expression.simplifier.DerivativeSimplifiers import *


from tests.utils import SimplifierTest, x, y, z


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
        self.assertSimplify((Sin(x) * x * Cos(x)) // x,
                            (Sin(x) // x) * x * Cos(x) + Sin(x) * (x // x) * Cos(x) + Sin(x) * x * (Cos(x) // x))


class DerivePowerTestCase(SimplifierTest):
    simplifier = DerivativeExponentSimplifier()

    def runTest(self):
        self.assertSimplify((x ^ 2) // x, Value(2) * (x ^ (Value(2) - 1)) * (x // x))


class DeriveExponentTestCase(SimplifierTest):
    simplifier = DerivativeExponentSimplifier()

    def runTest(self):
        self.assertSimplify((Value(2) ^ x) // x, Multiply(Value(2) ^ x, x // x, Log(2)))


class DerivativeConstantTestCase(SimplifierTest):
    simplifier = DerivativeConstantSimplifier()

    def runTest(self):
        self.assertSimplify(Value(2) // x, Value(0))
        self.assertSimplify(Value(2) // (x * 2), Value(0))


class DerivativeVariableTestCase(SimplifierTest):
    simplifier = DerivativeVariableSimplifier()

    def runTest(self):
        self.assertSimplify(x // x, Value(1))
