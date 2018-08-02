from parsing.Utils import isalpha
from parsing.Stream import Stream


def tokenize(s):
    stream = Stream(s.replace(' ', ''))
    last_token = ''
    tokens = []

    while stream.has_next():
        if len(last_token) == 0:
            last_token += stream.take()
            continue
        if (last_token + stream.peek()).isnumeric():
            last_token += stream.take()
            continue
        if isalpha(last_token + stream.peek()):
            last_token += stream.take()
            continue
        tokens.append(last_token)
        last_token = ''
    tokens.append(last_token)

    return tokens







