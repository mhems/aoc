from sys import argv
from typing import Set

def initial_bug_positions() -> Set[tuple[int, int, int]]:
    return {
        (x, y, 0)
        for y, line in enumerate(open(argv[1]))
        for x, cell in enumerate(line)
        if cell == '#'
    }

def add(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    return tuple(a + b for a, b in zip(p1, p2))

outer_corners = {
    (0, 0): {(2, 1), (1, 2)},
    (0, 4): {(1, 2), (2, 3)},
    (4, 0): {(2, 1), (3, 2)},
    (4, 4): {(3, 2), (2, 3)}
    }
inner_corners = {(1, 1), (1, 3), (3, 1), (3, 3)}
inner_edges = {
    (1, 2): {(0, y) for y in range(5)},
    (2, 1): {(x, 0) for x in range(5)},
    (2, 3): {(x, 4) for x in range(5)},
    (3, 2): {(4, y) for y in range(5)}
    }
deltas = [(0, -1), (0, 1), (-1, 0), (1, 0)]
def neighbors(position: tuple[int, int, int]) -> Set[tuple[int, int, int]]:
    x, y, depth = position
    full = {add(position, delta) for delta in deltas}
    real_w_depth = {(x, y, depth) for x, y in full if 0 <= x < 5 and 0 <= y < 5 and (x != 2 or y != 2)}
    
    if (x, y) in inner_corners:
        return real_w_depth
    ns = outer_corners.get((x, y))
    if ns is not None:
        return real_w_depth | {(x, y, depth-1) for x, y in ns}
    ns = inner_edges.get((x, y))
    if ns is not None:
        return real_w_depth | {(x, y, depth+1) for x, y in ns}
    if y == 0:
        outer = (2, 1, depth-1)
    elif y == 4:
        outer = (2, 3, depth-1)
    elif x == 0:
        outer = (1, 2, depth-1)
    else:
        outer = (3, 2, depth-1)
    return real_w_depth | {outer}

def num_adjacent_occupied(position: tuple[int, int, int],
                          positions: Set[tuple[int, int, int]]) -> int:
    return sum(int(n in positions) for n in neighbors(position))

def tick(positions: Set[tuple[int, int, int]]) -> Set[tuple[int, int, int]]:
    new_ps = {pos for pos in positions if num_adjacent_occupied(pos, positions) == 1}
    for pos in positions:
        for n in neighbors(pos):
            if n not in positions and 1 <= num_adjacent_occupied(n, positions) <= 2:
                new_ps.add(n)
    return new_ps

def cycle(positions: Set[tuple[int, int, int]], n: int) -> int:
    new_positions = set(positions)
    for _ in range(n):
        new_positions = tick(new_positions)
    return len(new_positions)

positions = initial_bug_positions()
print(cycle(positions, 10 if argv[1][0] == 'e' else 200))
