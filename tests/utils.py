import unittest


class SimplifierTest(unittest.TestCase):
    simplifier = None

    def simplify(self, expr):
        return self.simplifier.simplify(expr)

    def assertSimplify(self, expr1, expr2):
        self.assertEqual(self.simplify(expr1), expr2)


class SimplifyTest(unittest.TestCase):

    def assertSimplify(self, expr1, expr2):
        self.assertEqual(expr1.simplify(), expr2)
