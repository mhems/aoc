from sys import argv
from collections import namedtuple as nt

Concat = nt('Concat', ['elements'])
Or = nt('Or', ['a', 'b'])
Literal = nt('Literal', ['value'])

def parse_rules(lines: [str]) -> dict:
    ruleset = dict()
    for line in lines:
        left, right = line.strip().split(': ')
        if '"' in right:
            expr = Literal(right[1:-1])
        elif '|' in right:
            a, b = right.split('|')
            expr = Or(Concat([int(e) for e in a.split()]),
                      Concat([int(e) for e in b.split()]))
        else:
            expr = Concat([int(e) for e in right.split()])
        ruleset[int(left)] = expr
    return ruleset

def match(rules: dict, pattern: str) -> bool:
    pos = 0
    def inner_match(rule) -> bool:
        nonlocal pos
        if isinstance(rule, Literal):
            if pattern[pos] == rule.value:
                pos += 1
                return True
            return False
        if isinstance(rule, Or):
            original_pos = pos
            if inner_match(rule.a):
                return True
            pos = original_pos
            return inner_match(rule.b)
        for e in rule.elements:
            if not inner_match(rules[e]):
                return False
        return True
    return inner_match(rules[0]) and pos == len(pattern)

rules, patterns = open(argv[1]).read().split('\n\n')
rules = parse_rules(rules.split('\n'))
patterns = patterns.strip().split('\n')
print(sum(int(match(rules, pattern)) for pattern in patterns))
