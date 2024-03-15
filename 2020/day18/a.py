from sys import argv

def lex(expr: str) -> [str]:
    tokens = []
    for token in expr.split():
        while token.startswith('('):
            tokens.append('(')
            token = token[1:]
        i = 0
        while token.endswith(')'):
            i += 1
            token = token[:-1]
        tokens.append(token)
        for _ in range(i):
            tokens.append(')')
    return tokens

def shunting_yard(tokens: [str], equal: bool) -> [str]:
    output = []
    ops = []
    d = {'+': 2, '*': 1}
    for token in tokens:
        if token[0].isdigit():
            output.append(token)
        elif token in '+*':
            while ops and ops[-1] != '(' and (equal or d[ops[-1]] >= d[token]):
                output.append(ops.pop())
            ops.append(token)
        elif token == '(':
            ops.append(token)
        elif token == ')':
            while ops and ops[-1] != '(':
                output.append(ops.pop())
            ops.pop()
    while ops:
        output.append(ops.pop())
    return output    

def evaluate(expr: str, equal: bool = True) -> int:
    stack = []
    for e in shunting_yard(lex(expr), equal):
        if e == '+':
            stack.append(stack.pop() + stack.pop())
        elif e == '*':
            stack.append(stack.pop() * stack.pop())
        else:
            stack.append(int(e))
    return stack.pop()

lines = [line.strip() for line in open(argv[1]).readlines()]
print(sum(evaluate(line) for line in lines))
print(sum(evaluate(line, False) for line in lines))
