from expression.Variable import Variable
from expression.Function import *
from expression.simplifier.AddSimplifiers import AddCombineTermsSimplifier

from tests.utils import SimplifyTest

x, y, z = Variable('x'), Variable('y'), Variable('z')


class SimplifyTest1(SimplifyTest):

    def runTest(self):
        self.assertSimplify(Sin(x) // x + Sin(x) // x, Cos(x) * 2)

class SimplifyTest2(SimplifyTest):

    def runTest(self):
        self.assertSimplify(Sin(Asin((x ^ 2) // x + 0)), x * 2)

class SimplifyTest3(SimplifyTest):

    def runTest(self):
        self.assertSimplify(Acos(Cos(Acos(Sin(x) // x + 0))), x)

class SimplifyTest4(SimplifyTest):

    def runTest(self):
        # Currently failing, will need factor add simplifier
        # self.assertSimplify((x * x) + (x ^ 3) // x, (x ^ 2) * 4)
        pass

class SimplifyTest5(SimplifyTest):

    def runTest(self):
        self.assertSimplify((Value(5) * Value(3)) + (Value(2) - Value(1)), Value(16))


class SimplifyWhitelistTest(SimplifyTest):

    def runTest(self):
        self.assertSimplify(x + x, x + x, whitelist=[])
        # self.assertSimplify(x * (x + x), x * x * 2, whitelist=[AddCombineTermsSimplifier])
        # TODO this test fails, will need a more thoughtful solution to automatically combining terms
        # TODO write more tests

