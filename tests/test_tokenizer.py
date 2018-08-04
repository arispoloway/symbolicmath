import unittest

from parsing.Tokenizer import tokenize


class TokenizerTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual(tokenize('(34 + 3)'), ['(', '34', '+', '3', ')'])
        self.assertEqual(tokenize('(34 + xYz)'), ['(', '34', '+', 'xYz', ')'])
        self.assertEqual(tokenize('(34 - y * x+ xYz)'), ['(', '34', '-', 'y', '*', 'x', '+', 'xYz', ')'])
