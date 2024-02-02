from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

depth = int(lines[0].split()[1])
target = tuple(map(int, lines[1].split()[1].split(',')))

def make_cave(X: int, Y: int, depth: int) -> [[int]]:
    indices = [[None] * (X+1) for _ in range(Y+1)]
    levels = [[None] * (X+1) for _ in range(Y+1)]
    types = [[None] * (X+1) for _ in range(Y+1)]
    indices[0][0] = 0
    levels[0][0] = depth % 20183
    for x in range(1, X+1):
        indices[0][x] = x * 16807
        levels[0][x] = (indices[0][x] + depth) % 20183
    for y in range(1, Y+1):
        indices[y][0] = y * 48271
        levels[y][0] = (indices[y][0] + depth) % 20183
    for y in range(1, Y+1):
        for x in range(1, X+1):
            indices[y][x] = levels[y][x-1] * levels[y-1][x]
            levels[y][x] = (indices[y][x] + depth) % 20183
    indices[-1][-1] = 0
    levels[-1][-1] = depth % 20183
    for y in range(Y+1):
        for x in range(X+1):
            types[y][x] = levels[y][x] % 3
    return types

def print_cave(cave: [[int]]):
    for row in cave:
        for cell in row:
            print('.=|'[cell], end='')
        print()

def risk_level(cave: [[int]]) -> int:
    return sum(sum(row) for row in cave)

cave = make_cave(target[0], target[1], depth)
#print_cave(cave)
print(risk_level(cave))