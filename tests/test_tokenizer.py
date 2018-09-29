import unittest

from parsing.Tokenizer import tokenize, clean_tokens


class TokenizerTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual(tokenize('(34 + 3)'), ['(', '34', '+', '3', ')'])
        self.assertEqual(tokenize('(34 + xYz)'), ['(', '34', '+', 'xYz', ')'])
        self.assertEqual(tokenize('(34 - y * x+ xYz)'), ['(', '34', '-', 'y', '*', 'x', '+', 'xYz', ')'])
        self.assertEqual(tokenize('(34 // x)'), ['(', '34', '//', 'x', ')'])


class CleanTokensTest(unittest.TestCase):
    def runTest(self):
        self.assertEquals(clean_tokens(['x', 'sin', '(', 'x', ')']), ['x', '*', 'sin', '(', 'x', ')'])
