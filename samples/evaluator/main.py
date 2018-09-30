from parsing.Parser import parse_to_expression

if __name__ == '__main__':
    try:
        exp = parse_to_expression(input("Input an expression\n"))
    except Exception as e:
        print('Could not parse expression: {}'.format(e))
        quit(1)


    while True:
        i = input('Input a comma separated series of assignments, or q to quit (ex. "x=3,y=1")\n')
        if i == 'q':
            break
        assignments = i.replace(' ', '').split(',')
        mappings = {x[0]: float(x[1]) for x in map(lambda z: z.split('='), assignments)}
        print(exp.evaluate(**mappings))
