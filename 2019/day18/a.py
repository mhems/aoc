from sys import argv
from collections import deque
from heapq import heappush, heappop
from functools import cache

def parse_grid() -> tuple[list[list[str]], dict[str, tuple[int, int]]]:
    lines = [list(line.strip()) for line in open(argv[1]).readlines()]
    keys = {}
    for y, row in enumerate(lines):
        for x, cell in enumerate(row):
            if cell == '@' or cell.islower():
                keys[cell] = (y, x)
    return lines, keys

def neighbors(grid: list[list[str]], y: int, x: int):
    for dy, dx in ((-1, 0), (0, -1), (0, 1), (1, 0)):
        if grid[y+dy][x+dx] != '#':
            yield (y + dy, dx + x)

def walk(grid: list[list[str]], start: tuple[int, int]) -> dict[str, tuple[int, int]]:
    edges = dict()
    visited = set()
    q = deque([(start, 0, 0)])
    while q:
        (y, x), dist, doors = q.popleft()
        visited.add((y, x))
        cur = grid[y][x]
        if cur.islower() and dist != 0:
            edges[cur] = dist, doors
        for n in neighbors(grid, y, x):
            if n not in visited:
                next = grid[n[0]][n[1]]
                q.append((n, dist + 1, doors | (to_bit(next) if next.isupper() else 0)))
    return edges

@cache
def to_bit(key: str) -> int:
    return 1 << (ord(key.lower()) - ord('a'))

def solve(cliques) -> int:
    q = []
    targets = []
    total = 0
    N = len(cliques)
    for i, clique in enumerate(cliques):
        mask = 0
        for v in clique.keys():
            if v != '@':
                distance, doors = clique['@'][v]
                mask |= to_bit(v)
                if doors == 0:
                    positions = ['@'] * N
                    positions[i] = v
                    heappush(q, (distance, tuple(positions), to_bit(v)))
        total |= mask
        targets.append(mask)
    visited = dict()
    while q:
        num_steps, positions, collected = heappop(q)
        if num_steps >= visited.get((positions, collected), 1e6):
            continue
        visited[(positions, collected)] = num_steps
        if collected == total:
            return num_steps
        for i, (position, clique, target) in enumerate(zip(positions, cliques, targets)):
            if target & collected == target:
                continue
            for v, (w, required) in clique[position].items():
                if v != '@' and to_bit(v) & collected == 0:
                    if required & collected == required:
                        new_positions = list(positions)
                        new_positions[i] = v
                        heappush(q, (num_steps + w, tuple(new_positions), collected | to_bit(v)))

def quadsect(grid: list[list[str]], start: tuple[int, int]) -> list[tuple[int, int]]:
    y, x = start
    grid[y-1][x-1] = '@'
    grid[y-1][x] = '#'
    grid[y-1][x+1] = '@'
    grid[y][x-1] = '#'
    grid[y][x] = '#'
    grid[y][x+1] = '#'
    grid[y+1][x-1] = '@'
    grid[y+1][x] = '#'
    grid[y+1][x+1] = '@'
    return [(y-1, x-1), (y-1, x+1), (y+1, x-1), (y+1, x+1)]    

grid, keys = parse_grid()
clique = {key: walk(grid, pos) for key, pos in keys.items()}
print(solve([clique]))

starts = quadsect(grid, keys['@'])
quads = [walk(grid, start) for start in starts]
cliques = [{'@': keyset} for keyset in quads]
for keyset, clique in zip(quads, cliques):
    for key in keyset.keys():
        clique[key] = walk(grid, keys[key])
print(solve(cliques))
