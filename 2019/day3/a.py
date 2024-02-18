from sys import argv

with open(argv[1]) as fp:
    a, b = [line.strip().rstrip(',').split(',') for line in fp.readlines()]

def trace(path: [str]) -> (set, {(int, int): int}):
    visited = set()
    deltas = {'R': (0, 1), 'L': (0, -1), 'D': (1, 0), 'U': (-1, 0)}
    pos = (0, 0)
    d = {}
    i = 0
    for step in path:
        delta, amt = deltas[step[0]], int(step[1:])
        for _ in range(amt):
            pos = (pos[0] + delta[0], pos[1] + delta[1])
            visited.add(pos)
            i += 1
            d[pos] = i
    return visited, d

def closest_intersection(a: [str], b: [str]) -> int:
    return min(abs(x) + abs(y) for x, y in trace(a)[0].intersection(trace(b)[0]))

def shortest_intersection(a: [str], b: [str]) -> int:
    path_a, a_dict = trace(a)
    path_b, b_dict = trace(b)
    intersections = path_a.intersection(path_b)
    return min(a_dict[pos] + b_dict[pos] for pos in intersections)

print(closest_intersection(a, b))
print(shortest_intersection(a, b))
