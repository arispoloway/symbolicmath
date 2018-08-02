import unittest

from expression.Function import Sin, Cos

from expression.Derivative import Derivative


class DeriveSinTestCase(unittest.TestCase):
    def runTest(self):
        expr = Derivative(Sin('x') - 1, 'x').reduce().reduce()
        self.assertEqual(expr, Cos('x'))

if __name__ == '__main__':
    unittest.main()

