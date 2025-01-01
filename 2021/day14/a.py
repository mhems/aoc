from sys import argv
from collections import Counter, defaultdict
from itertools import pairwise

def frequency(counter: Counter, last: str) -> int:
    element_counts = defaultdict(int, [(last, 1)])
    for (a, _), f in counter.items():
        element_counts[a] += f
    ordered = Counter(element_counts).most_common()
    return ordered[0][1] - ordered[-1][1]        

def insert(polymer: str, rules: {str: str}, n: int) -> int:
    counter = Counter(a + b for a, b in pairwise(polymer))
    for _ in range(n):
        new_counter = defaultdict(int)
        for p, f in counter.items():
            new_counter[p[0] + rules[p]] += f
            new_counter[rules[p] + p[1]] += f
        counter = new_counter
    return frequency(counter, polymer[-1])

chunks = open(argv[1]).read().split('\n\n')
polymer = chunks[0].strip()
rules = dict(line.strip().split(' -> ') for line in chunks[1].strip().split('\n'))
print(insert(polymer, rules, 10))
print(insert(polymer, rules, 40))
