from sys import argv
from collections import defaultdict

rules, updates = open(argv[1]).read().split('\n\n')
rules = [tuple(map(int, rule.strip().split('|'))) for rule in rules.split('\n')]
updates = [tuple(map(int, page.strip().split(','))) for page in updates.strip().split('\n')]

def ordered(update: [int], rules: [(int, int)]) -> bool:
    def get_index(e):
        try:
            return update.index(e)
        except ValueError:
            return -1
    for x, y in rules:
        x_index = get_index(x)
        y_index = get_index(y)
        if x_index != -1 and y_index != -1 and y_index < x_index:
            return False
    return True

def bisect(itr, predicate) -> (list, list):
    meets = []
    fails = []
    for element in itr:
        if predicate(element):
            meets.append(element)
        else:
            fails.append(element)
    return meets, fails

def order(update: [int], rules: [(int, int)]) -> [[int]]:
    applicable = [(x, y) for x, y in rules if x in update and y in update]
    follows = defaultdict(set)
    for x, y in applicable:
        follows[x].add(y)
    return sorted(follows.keys(), key=lambda k: len(follows[k]), reverse=True)

def sum_middle_pages(updates: [[int]]) -> int:
    return sum(update[len(update)//2] for update in updates)

in_order, out_order = bisect(updates, lambda update: ordered(update, rules))
print(sum_middle_pages(in_order))
print(sum_middle_pages(order(update, rules) for update in out_order))