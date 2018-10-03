class Stream(object):
    """
    A stream object supporting peek, take, and has_next
    """
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


class Queue(object):
    """
    A queue supporting these operations: push, pop, is_empty
    """
    def __init__(self):
        self._list = []

    def push(self, x):
        self._list.append(x)

    def pop(self):
        if len(self._list) > 0:
            return self._list.pop(0)
        raise IndexError()

    def as_list(self):
        return self._list[::]

    def is_empty(self):
        return len(self._list) == 0


class Stack(object):
    """
    A stack object supporting the push, pop, peek, and is_empty operations
    """
    def __init__(self):
        self._list = []

    def push(self, x):
        self._list.append(x)

    def pop(self):
        if len(self._list) > 0:
            return self._list.pop()
        raise IndexError()

    def peek(self):
        if len(self._list) > 0:
            return self._list[-1]
        raise IndexError()

    def is_empty(self):
        return len(self._list) == 0