from sys import argv
from math import prod

def parse_rule(line: str) -> (str, [(int, int)]):
    left, right = line.split(': ')
    return left, [tuple(map(int, token.strip().split('-'))) for token in right.strip().split(' or ')]

def in_a_range(num: int, ranges: [(int, int)]) -> bool:
    for lower, upper in ranges:
        if lower <= num <= upper:
            return True
    return False

def impossible(num: int, rules: (str, [(int, int)])) -> bool:
    return all(not in_a_range(num, rule) for _, rule in rules)

def error_rate(rules: (str, [(int, int)]), tickets: [[int]]) -> (int, [[int]]):
    rate = 0
    valid_tickets = []
    for ticket in tickets:
        valid = True
        for field in ticket:
            if impossible(field, rules):
                rate += field
                valid = False
        if valid:
            valid_tickets.append(ticket)
    return rate, valid_tickets

def fix(mapping: {str: {int}}, name: str, fixed: {int}):
    set_ = mapping[name]
    if len(set_) == 1:
        found = next(iter(set_))
        fixed.add(found)
        for k, s in mapping.items():
            if k != name and found in s:
                s.remove(found)
                if len(s) == 1:
                    fix(mapping, k, fixed)

def deduce(rules: (str, [(int, int)]), candidates: [[int]]) -> {str: int}:
    mapping = {field: set(range(len(rules))) for field, _ in rules}
    fixed = set()
    while any(len(s) > 1 for s in mapping.values()):
        for name, ranges in rules:
            for index in range(len(rules)):
                if index not in fixed:
                    for ticket in candidates:
                        if not in_a_range(ticket[index], ranges):
                            if index in mapping[name]:
                                mapping[name].remove(index)
                                fix(mapping, name, fixed)
    return {k: s.pop() for k, s in mapping.items()}

rules, mine, other = open(argv[1]).read().strip().split('\n\n')
rules = [parse_rule(line.strip()) for line in rules.split('\n')]
mine = [int(e) for e in mine.split('\n')[1].split(',')]
others = [[int(e) for e in line.strip().split(',')] for line in other.split('\n')[1:]]

rate, valid_tickets = error_rate(rules, others)
print(rate)
mapping = deduce(rules, valid_tickets + [mine])
print(prod(mine[v] for k, v in mapping.items() if k.startswith('departure')))