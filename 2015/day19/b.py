from sys import argv
from random import choice

with open(argv[1]) as fp:
    text = fp.read()

rules, mol = text.strip().split('\n\n')
rules = [tuple(line.strip().split(' => ')) for line in rules.split('\n')]
rules = {rule[1]: rule[0] for rule in rules}

def count_derivation(mol: str, rules: {str:str}, limit: int = 1000) -> int:
    count = 0
    i = 0
    replacements = list(rules.keys())
    while mol != "e" and i < limit:
        rule = choice(replacements)
        if rule in mol:
            mol = mol.replace(rule, rules[rule], 1)
            count += 1
        i += 1
    return count if mol == "e" else limit

answer = min(count_derivation(mol, rules) for _ in range(10000))
print(answer)
