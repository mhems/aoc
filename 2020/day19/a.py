from sys import argv
from collections import namedtuple as nt
from itertools import batched

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

def match_rule(rules: dict, pattern: str, first: bool) -> bool:
    def inner_match(rule, start: int = 0) -> (bool, int):
        if isinstance(rule, Literal):
            if pattern[start] == rule.value:
                return (True, start + 1)
            return (False, start)
        elif isinstance(rule, Or):
            matched, new_pos = inner_match(rule.a, start)
            if matched:
                return (True, new_pos)
            matched, new_pos = inner_match(rule.b, start)
            if matched:
                return (True, new_pos)
            return (False, start)
        elif isinstance(rule, Concat):
            pos = start
            for e in rule.elements:
                matched, new_pos = inner_match(rules[e], pos)
                if matched:
                    pos = new_pos
                else:
                    return (False, pos)
            return (True, pos)
    rule = 42 if first else 31
    return inner_match(rules[rule])[0]

def match(rules: dict, pattern: str, part1: bool = True) -> bool:
    # notice that rules 42 and 31 are mutually exclusive and only match 8-length strings
    octets = [''.join(batch) for batch in batched(pattern, 8)]
    num_octets = len(octets)
    # part1 regex is 42^m 31^n where m is 2 and n is 1
    if part1:
        return (num_octets == 3 and
                match_rule(rules, octets[0], True) and
                match_rule(rules, octets[1], True) and
                match_rule(rules, octets[2], False))
    # part2 regex is same except m >= n + 1
    # ambiguity is where to stop 42 and find n matches of 31
    # must match 42 at least twice and then 31 at least once
    # keep matching 42 until you cannot, then match 31 until the end
    i = 0
    while i < num_octets and match_rule(rules, octets[i], True):
        i += 1
    if i < 2:
        return False
    div = i
    while i < num_octets and match_rule(rules, octets[i], False):
        i += 1
    return i == num_octets and div > num_octets - div and num_octets - div >= 1

rules, patterns = open(argv[1]).read().split('\n\n')
rules = parse_rules(rules.split('\n'))
patterns = patterns.strip().split('\n')

print(sum(int(match(rules, pattern)) for pattern in patterns))
print(sum(int(match(rules, pattern, False)) for pattern in patterns))
