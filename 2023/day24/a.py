from sys import argv
from itertools import combinations

if argv[1][0] == 'e':
    lo, hi = 7, 27
else:
    lo, hi = 200000000000000, 400000000000000

def add(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    return tuple(a+b for a, b in zip(p1, p2))

def diff(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    return tuple(a-b for a, b in zip(p1, p2))

def mul(p1: tuple[int, int], n: int) -> tuple[int, int]:
    x, y = p1
    return x*n, y*n

def cross(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    x1, y1 = p1
    x2, y2 = p2
    return x1*y2 - x2*y1

def sign(n: float) -> int:
    if n == 0:
        return 0
    return 1 if n > 0 else -1

def orient(a: tuple[int, int], b: tuple[int, int], c: tuple[int, int]) -> int:
    return sign(cross(diff(b, a), diff(c, a)))

def lines_intersect(a: tuple[int, int], b: tuple[int, int], c: tuple[int, int], d: tuple[int, int]) -> bool:
    o1, o2, o3, o4 = [orient(e1, e2, p) for e1, e2, p in ((a, b, c), (a, b, d), (c, d, a), (c, d, b))]
    return o1 * o2 < 0 and o3 * o4 < 0

def rays_intersect(a, b) -> bool:
    def clip(p: tuple[int, int], d: tuple[int, int]):
        x1 = (lo - p[0]) / d[0]
        x2 = (hi - p[0]) / d[0]
        y1 = (lo - p[1]) / d[1]
        y2 = (hi - p[1]) / d[1]
        xmin = min(x1, x2)
        xmax = max(x1, x2)
        ymin = min(y1, y2)
        ymax = max(y1, y2)
        tmin = max(xmin, ymin, 0)
        tmax = min(xmax, ymax)
        if tmin > tmax:
            return None
        return tmin, tmax
    P, r = a
    Q, s = b
    ta = clip(P, r)
    tb = clip(Q, s)
    if ta is None or tb is None:
        return False
    tmina, tmaxa = ta
    tminb, tmaxb = tb
    return lines_intersect(add(P, mul(r, tmina)), add(P, mul(r, tmaxa)),
                           add(Q, mul(s, tminb)), add(Q, mul(s, tmaxb)))
    
def num_intersections(rays: list[tuple[tuple[int, int], tuple[int, int]]]) -> int:
    return sum(int(rays_intersect(((x1, y1), (dx1, dy1)), ((x2, y2), (dx2, dy2)))) for ((x1, y1, _), (dx1, dy1, _)), ((x2, y2, _), (dx2, dy2, _)) in combinations(rays, 2))

def parse(line) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    return tuple(tuple(int(e) for e in vector.split(', ')) for vector in line.strip().split('@'))

rays = [parse(line) for line in open(argv[1]).readlines()]
print(num_intersections(rays))
