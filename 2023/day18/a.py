from sys import argv
from collections import namedtuple as nt

deltas = {'R': (0, 1), 'U': (-1, 0), 'D': (1, 0), 'L': (0, -1)}

Step = nt('Step', ['dir', 'num'])

def parse() -> tuple[list[Step], list[Step]]:
    part1 = []
    part2 = []
    with open(argv[1]) as fp:
        for line in fp.readlines():
            dir, num, color = line.strip().split()
            part1.append(Step(dir, int(num)))
            s = color.strip('()')[1:]
            dir, num = 'RDLU'[int(s[-1])], int(s[:-1], base=16)
            part2.append(Step(dir, num))
    return part1, part2

def get_points(steps: list[Step]) -> list[tuple[int, int]]:
    points = []
    pos = (0, 0)
    points.append(pos)
    perimeter = 0
    for step in steps:
        perimeter += step.num        
        pos = tuple(p + d*step.num for p, d in zip(pos, deltas[step.dir]))
        points.append(pos)
    return points, perimeter

def area(steps: list[Step]) -> int:
    points, perimeter = get_points(steps)
    N = len(points)
    A = sum(x * (points[(i+1)%N][0] - points[(i-1)%N][0]) for i, (_, x) in enumerate(points)) // 2
    return A + perimeter//2 + 1

part1, part2 = parse()
print('\n'.join(map(str, (area(part) for part in parse()))))
