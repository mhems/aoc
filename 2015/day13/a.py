from sys import argv
from itertools import permutations, pairwise

with open(argv[1]) as fp:
    lines = fp.readlines()

edges = {}
people = set()
for line in lines:
    tokens = line.strip().strip('.').split()
    delta = int(tokens[3])
    if tokens[2] == 'lose':
        delta = -delta
    edges[(tokens[0], tokens[-1])] = delta
    people.add(tokens[0])
    people.add(tokens[-1])

def generate_seatings(people: {str}):
    for perm in permutations(people):
        l = list(perm)
        l.append(l[0])
        yield l

def seating_value(seating: [str]):
    return sum(edges[pair] + edges[(pair[1], pair[0])] for pair in pairwise(seating))

print(max(seating_value(seating) for seating in generate_seatings(people)))
