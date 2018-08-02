import unittest
from expression.Utils import reduce_x
from expression.Function import Sin, Add, Multiply
from expression.Variable import Variable

from expression.Value import Value

class AddReduceTestCase(unittest.TestCase):
    def runTest(self):
        self.assertEqual((Variable('x') + Sin('x') + 3 + 4).reduce(), Add(Value(7), Variable('x'), Sin('x')))
        #TODO fix this failing test - probably will require somewhat overhauling the reduction system
        self.assertEqual((Variable('x') + Variable('x') + Variable('x')).reduce(), Value(3) * 'x')

class MultiplyReduceTestCase(unittest.TestCase):
    def runTest(self):
        expr = (Variable('x') * 3 * 4 * Sin('x')).reduce().reduce().reduce()
        self.assertEqual(expr, Multiply(Value(12), Variable('x'), Sin('x')))

if __name__ == '__main__':
    unittest.main()

