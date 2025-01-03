from sys import argv
from sympy import Ray
from itertools import combinations
from tqdm import tqdm

def parse2d(line) -> Ray:
    p, v = map(lambda l: [int(e) for e in l.split(', ')[:-1]], line.strip().split('@'))
    return Ray(p, tuple(a + b for a, b in zip(p, v)))

def num_intersections(rays: [Ray], bounds: (int, int)) -> int:
    count = 0
    combos = list(combinations(rays, 2))
    for r1, r2 in tqdm(combos):
        p = r1.intersection(r2)
        if p and all(bounds[0] <= e <= bounds[1] for e in p[0]):
            count += 1
    return count

rays2d = [parse2d(line) for line in open(argv[1]).readlines()]
print(num_intersections(rays2d, (200000000000000, 400000000000000)))
