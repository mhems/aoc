from sys import argv
from functools import reduce
from collections import defaultdict

def count_easy(lines: [([str], [str])]) -> int:
    num_easy = 0
    for _, output in lines:
        for num in output:
            if len(num) in (2, 3, 4, 7):
                num_easy += 1
    return num_easy

def decode(patterns: [str], output: [str]) -> int:
    components = {
        0: set([0, 1, 2, 4, 5, 6]),
        1: set([2, 5]),
        2: set([0, 2, 3, 4, 6]),
        3: set([0, 2, 3, 5, 6]),
        4: set([1, 2, 3, 5]),
        5: set([0, 1, 3, 5, 6]),
        6: set([0, 1, 3, 4, 5, 6]),
        7: set([0, 2, 5]),
        8: set([0, 1, 2, 3, 4, 5, 6]),
        9: set([0, 1, 2, 3, 5, 6])
    }
    mapping = {i : None for i in range(7)}
    by_length = defaultdict(set)
    for pattern in patterns:
        by_length[len(pattern)].add(pattern)
    intersections = {k: reduce(lambda s, t: s.intersection(t),
                               (set(e) for e in v))
                     for k, v in by_length.items()}
    cands_5 = reduce(lambda a, b: set(a).intersection(set(b)), by_length[5])
    cands_6 = reduce(lambda a, b: set(a).intersection(set(b)), by_length[6])
    mapping[0] = (intersections[3] - intersections[2]).pop()
    mapping[3] = (cands_5 - cands_6).pop()
    mapping[2] = (intersections[2] - cands_6).pop()
    mapping[6] = (cands_5 - {mapping[0]} - {mapping[3]}).pop()
    mapping[5] = (intersections[2] - {mapping[2]}).pop()
    mapping[1] = (cands_6 - {mapping[0]} - {mapping[5]} - {mapping[6]}).pop()
    mapping[4] = (intersections[7] - reduce(lambda s, t: s.union(t),
                                            ({mapping[i]} for i in (0, 1, 2, 3, 5, 6)))).pop()
    mapping = {v: k for k, v in mapping.items()}
    num = ''
    for o in output:
        segments = set(mapping[letter] for letter in o)
        for v, s in components.items():
            if segments == s:
                num += str(v)
                break
    return int(num)

lines = [tuple(map(lambda s: s.strip().split(), line.strip().split('|'))) for line in open(argv[1]).readlines()]
print(count_easy(lines))
print(sum(decode(pattern, output) for pattern, output in lines))
