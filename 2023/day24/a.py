from sys import argv
from itertools import combinations
import numpy as np
import sympy as sp

def lines_intersect(a, b, c, d) -> bool:
    cross = lambda a, b: a[0] * b[1] - a[1] * b[0]
    o1, o2, o3, o4 = [np.sign(cross(e2 - e1, p - e1)) for e1, e2, p in ((a, b, c), (a, b, d), (c, d, a), (c, d, b))]
    return o1 * o2 < 0 and o3 * o4 < 0

def rays_intersect(a, b, bounds) -> bool:
    lo, hi = bounds
    def clip(p, d):
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
    return lines_intersect(P + r * tmina, P + r * tmaxa, Q + s * tminb, Q + s * tmaxb)

def num_intersections(rays, bounds) -> int:
    trio = set()

    def add_if_not_parallel(p, d):
        if all(np.cross(d, d_other).any() for _, d_other in trio):
            trio.add((tuple(p), tuple(d)))

    num = 0
    for r1, r2 in combinations(rays, 2):
        p1, d1 = r1
        p2, d2 = r2
        if rays_intersect((p1[:-1], d1[:-1]), (p2[:-1], d2[:-1]), bounds):
            num += 1
        if len(trio) < 3 and np.cross(d1, d2).any():
            add_if_not_parallel(p1, d1)
            add_if_not_parallel(p2, d2)
    a, b, c, *_ = trio
    return num, solve(a, b, c)

def solve(a, b, c) -> int:
    (h1p, h1v), (h2p, h2v), (h3p, h3v) = ((np.array(p), np.array(d)) for p, d in (a, b, c))
    dv12 = h1v - h2v
    dp12 = h1p - h2p
    dv13 = h1v - h3v
    dp13 = h1p - h3p
    C12 = np.cross(h2p, h2v) - np.cross(h1p, h1v)
    C13 = np.cross(h3p, h3v) - np.cross(h1p, h1v)
    system = sp.Matrix([
        [0, dv12[2], -dv12[1], 0, dp12[2], -dp12[1], -C12[0]],
        [-dv12[2], 0, dv12[0], -dp12[2], 0, dp12[0], -C12[1]],
        [dv12[1], -dv12[0], 0, dp12[1], -dp12[0], 0, -C12[2]],
        [0, dv13[2], -dv13[1], 0, dp13[2], -dp13[1], -C13[0]],
        [-dv13[2], 0, dv13[0], -dp13[2], 0, dp13[0], -C13[1]],
        [dv13[1], -dv13[0], 0, dp13[1], -dp13[0], 0, -C13[2]]
    ])
    rref, pivots = system.rref()
    assert len(pivots) == 6
    return rref[6] + rref[13] + rref[20]

bounds = (7, 27) if argv[1][0] == 'e' else (2e14, 4e14)
rays = [tuple(np.array([int(e) for e in vector.split(', ')], dtype=int) for vector in line.strip().split('@'))
        for line in open(argv[1]).readlines()]
print('\n'.join(map(str, num_intersections(rays, bounds))))
