from parsing.Tokenizer import tokenize, Stream


class Parser(object):
    def __init__(self, s):
        self._tokens = tokenize(s)
        self._stream = Stream(self._tokens)

