from collections import namedtuple as nt
import re

Plot = nt('Plot', ['i', 'x', 'y', 'w', 'h'])
regex = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

with open('input.txt') as fp:
    lines = fp.readlines()

def parse_plot(line: str) -> Plot:
    return Plot(*map(int, re.match(regex, line.strip()).groups()))

def make_grid(plots: [Plot]) -> [[int]]:
    xs = [plot.x + plot.w for plot in plots]
    ys = [plot.y + plot.h for plot in plots]
    X = max(xs)
    Y = max(ys)
    return [[0] * X for _ in range(Y)]

def score(grid: [[int]], plots: [Plot]) -> int:
    for plot in plots:
        for r in range(plot.y, plot.y + plot.h):
            for c in range(plot.x, plot.x + plot.w):
                grid[r][c] += 1
    return sum(sum(int(cell >= 2) for cell in row) for row in grid)

def find_intact(R: int, C: int, plots: [Plot]) -> int:
    claims = [[0] * C for _ in range(R)]
    intact = set(plot.i for plot in plots)
    for plot in plots:
        for r in range(plot.y, plot.y + plot.h):
            for c in range(plot.x, plot.x + plot.w):
                if claims[r][c] > 0:
                    claim = claims[r][c]
                    if claim in intact:
                        intact.remove(claim)
                    if plot.i in intact:
                        intact.remove(plot.i)
                else:
                    claims[r][c] = plot.i
    return next(iter(intact))

plots = [parse_plot(line.strip()) for line in lines]
grid = make_grid(plots)
print(score(grid, plots))
print(find_intact(len(grid), len(grid[0]), plots))
