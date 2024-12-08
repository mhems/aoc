from sys import argv
from collections import defaultdict
from itertools import combinations
from functools import reduce

def parse(grid: [[str]]) -> {str: {(int, int)}}:
    nodes = defaultdict(set)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != '.':
                nodes[cell].add((y, x))
    return nodes

def find_antinodes(locs: {(int, int)}, Y: int, X: int, endless: bool) -> {(int, int)}:
    antinodes = set()
    for a, b in combinations(locs, 2):
        dy, dx = a[0] - b[0], a[1] - b[1]
        if not endless:
            antinodes.add((a[0] + dy, a[1] + dx))
            antinodes.add((b[0] - dy, b[1] - dx))
        else:
            pos = a
            while True:
                antinodes.add(pos)
                if 0 <= pos[0] < Y and 0 <= pos[1] < X:
                    pos = (pos[0] + dy, pos[1] + dx)
                else:
                    break
            pos = b
            while True:
                antinodes.add(pos)
                if 0 <= pos[0] < Y and 0 <= pos[1] < X:
                    pos = (pos[0] - dy, pos[1] - dx)
                else:
                    break
    return {(y, x) for y, x in antinodes if 0 <= y < Y and 0 <= x < X}

def find_all_antinodes(nodes: {str: {(int, int)}}, Y: int, X: int, endless: bool = False) -> {(int, int)}:
    return len(reduce(lambda s1, s2: s1 | s2,
                      [find_antinodes(locations, Y, X, endless) for locations in nodes.values()]))

grid = [list(line.strip()) for line in open(argv[1]).readlines()]
nodes = parse(grid)
print(find_all_antinodes(nodes, len(grid), len(grid[0])))
print(find_all_antinodes(nodes, len(grid), len(grid[0]), True))
