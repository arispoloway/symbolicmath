from parsing.Utils import is_alpha, Stream, is_numeric


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
        if is_alpha(last_token + stream.peek()):
            last_token += stream.take()
            continue
        # TODO come up with cleaner way to handle multi character operators
        if (last_token + stream.peek()) == '/':
            last_token += stream.take()
            continue
        if (last_token + stream.peek()) == '//':
            last_token += stream.take()
        tokens.append(last_token)
        last_token = ''
    tokens.append(last_token)

    return tokens


def clean_tokens(tokens):
    tokens = tokens[::]
    idx = 0
    while idx < (len(tokens) - 1):
        if is_alpha(tokens[idx]) and is_alpha(tokens[idx + 1]):
            tokens.insert(idx + 1, '*')

        # TODO see if this is the best way to do this
        if (is_alpha(tokens[idx]) and is_numeric(tokens[idx + 1])) or\
                (is_numeric(tokens[idx]) and is_alpha(tokens[idx + 1])):
            tokens.insert(idx + 1, '*')

        idx += 1
    return tokens
