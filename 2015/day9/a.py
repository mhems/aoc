from sys import argv
from itertools import permutations, pairwise

with open(argv[1]) as fp:
    lines = fp.readlines()

edges = {}
cities = set()
for line in lines:
    tokens = line.strip().split()
    cities.add(tokens[0])
    cities.add(tokens[2])
    edges[(tokens[0], tokens[2])] = int(tokens[4])
    edges[(tokens[2], tokens[0])] = edges[(tokens[0], tokens[2])]

def tour_length(path: [str]) -> int:
    return sum(edges[pair] for pair in pairwise(path))

answer = min(tour_length(path) for path in permutations(cities))
print(answer)

answer = max(tour_length(path) for path in permutations(cities))
print(answer)