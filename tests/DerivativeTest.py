import unittest

from Function import Sin, Cos, Multiply, Add
from Value import Value
from Variable import Variable
from Derivative import Derivative


class DeriveSinTestCase(unittest.TestCase):
    def runTest(self):
        x = Derivative(Sin(Variable('x')), 'x').reduce().reduce().reduce()
        self.assertEqual(Derivative(Sin(Variable('x')), 'x').reduce().reduce(), Cos(Variable('x')))

if __name__ == '__main__':
    unittest.main()

