from parsing.Tokenizer import tokenize, clean_tokens
from parsing.Utils import (
    Stream,
    Queue,
    Stack,
    is_alpha,
    parse_number,
    is_numeric,
    is_operator,
    is_function,
    get_associativity,
    get_precedence,
    get_operator,
    get_function,
    get_function_args,
)
from expression.Value import Value
from expression.Variable import Variable


def shunting_yard(tokens):
    s = Stream(tokens)
    output_queue = Queue()
    operator_stack = Stack()
    while s.has_next():
        t = s.take()
        if is_numeric(t):
            output_queue.push(t)
        elif is_function(t):
            operator_stack.push(t)
        elif is_operator(t):
            # TODO make this nicer
            while not operator_stack.is_empty():
                n = operator_stack.peek()
                if n != '(' and \
                        (is_function(n) or
                        (get_precedence(n) > get_precedence(t)) or
                        (get_precedence(n) == get_precedence(t) and get_associativity(n) == 'l')):
                    output_queue.push(operator_stack.pop())
                else:
                    break
            operator_stack.push(t)
        elif t == '(':
            operator_stack.push(t)
        elif t == ')':
            while operator_stack.peek() != '(':
                output_queue.push(operator_stack.pop())
            operator_stack.pop()
        elif t == ',':
            pass
        elif is_alpha(t):
            output_queue.push(t)
    while not operator_stack.is_empty():
        output_queue.push(operator_stack.pop())

    return output_queue


def parse_to_expression(s):
    tokens = tokenize(s)
    tokens = clean_tokens(tokens)
    queue = shunting_yard(tokens)

    stack = Stack()

    while not queue.is_empty():
        t = queue.pop()
        if is_numeric(t):
            stack.push(Value(parse_number(t)))
        elif is_function(t):
            arg_num = get_function_args(t)
            args = [stack.pop() for _ in range(arg_num)]
            args.reverse()
            stack.push(get_function(t)(*args))
        elif is_operator(t):
            v2, v1 = stack.pop(), stack.pop()
            stack.push(get_operator(t)(v1, v2))
        else:
            stack.push(Variable(t))

    return stack.pop()




