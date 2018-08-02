class Stream(object):
    def __init__(self, s):
        self._s = s
        self._pos = 0
        self._len = len(s)

    def peek(self, ahead=0):
        idx = self._pos + ahead
        if idx >= self._len:
            return None
        return self._s[self._pos + ahead]

    def take(self):
        self._pos += 1
        return self._s[self._pos - 1]

    def has_next(self):
        return self._pos < self._len
