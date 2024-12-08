from sys import argv
from collections import namedtuple as nt
from itertools import product

Eq = nt('Eq', ['operands', 'result'])

def make_eq(text: str) -> Eq:
    tokens = text.split(': ')
    return Eq(list(map(int, tokens[1].split())), int(tokens[0]))

def satisfiable(eq: Eq, n: int = 2) -> bool:
    for combo in product(range(n), repeat=len(eq.operands) - 1):
        operators = list(combo)
        result = eq.operands[0]
        for i in range(len(operators)):
            if operators[i] == 0:
                result += eq.operands[i+1]
            elif operators[i] == 1:
                result *= eq.operands[i+1]
            elif operators[i] == 2:
                result = int(str(result) + str(eq.operands[i+1]))
            if result > eq.result:
                break
        if result == eq.result:
            return True
    return False

eqs = [make_eq(line.strip()) for line in open(argv[1]).readlines()]
s1, s2 = 0, 0
for eq in eqs:
    if satisfiable(eq):
        s1 += eq.result
    elif satisfiable(eq, 3):
        s2 += eq.result
print(s1)
print(s1 + s2)
