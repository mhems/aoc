from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

# https://www.redblobgames.com/grids/hexagons/#distances-cube
def distance(path: [str]) -> [int]:
    pos = (0, 0, 0) # q s r
    deltas = {'n': (0, 1, -1), 'ne': (1, 0, -1), 'nw': (-1, 1, 0),
              's': (0, -1, 1), 'se': (1, -1, 0), 'sw': (-1, 0, 1)}
    distances = []
    for step in path:
        pos = tuple(sum(t) for t in zip(pos, deltas[step]))
        distances.append(sum(map(abs, pos)) // 2)
    return distances

paths = [line.strip().split(',') for line in lines]
lengths = [distance(path) for path in paths]
print([length[-1] for length in lengths])
print([max(length) for length in lengths])
