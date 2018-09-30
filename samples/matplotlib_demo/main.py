import matplotlib.pyplot as plt
from parsing.Parser import parse_to_expression


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


def read_input(prompt):
    try:
        i = input("{}\n".format(prompt))
        return i
    except Exception as e:
        return None


def input_verify(prompt, verification):
    while True:
        try:
            return verification(read_input(prompt))
        except Exception as e:
            print("Invalid input\n")


num_exprs = input_verify("How many expressions?", int)
exprs = []
for i in range(num_exprs):
    exprs.append(input_verify("Input an expression in terms of x", parse_to_expression))

xmin = input_verify("Input xmin", float)
xmax = input_verify("Input xmax", float)
xstep = input_verify("Input xstep", float)

steps = list(frange(xmin, xmax, xstep))
values = [[exp.evaluate(x=p).get_numeric_value() for p in steps] for exp in exprs]

for i, e in enumerate(values):
    plt.plot(steps, e, label=str(exprs[i]))
plt.legend()
plt.show()


