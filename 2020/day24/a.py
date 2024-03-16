from sys import argv
from collections import defaultdict
from collections import namedtuple as nt

Hex = nt('Hex', ['q', 'r', 's'])

def generate(path: str):
    pos = 0
    while pos < len(path):
        if path[pos] in 'ns':
            yield path[pos: pos+2]
            pos += 2
        else:
            yield path[pos]
            pos += 1

def walk(path: str, black: {Hex: bool}):
    pos = (0, 0, 0)
    for step in generate(path):
        pos = tuple(sum(t) for t in zip(pos, deltas[step]))
    if pos in black:
        black[pos] = not black[pos]
    else:
        black[pos] = True

def num_black(d: dict) -> int:
    return sum(int(v) for v in d.values())

# largely adapted from https://www.redblobgames.com/grids/hexagons/#distances-cube
deltas = {'e': (1, 0, -1), 'ne': (1, -1, 0), 'nw': (0, -1, 1),
          'w': (-1, 0, 1), 'se': (0, 1, -1), 'sw': (-1, 1, 0)}
cube_direction_vectors = [Hex(+1, 0, -1), Hex(+1, -1, 0), Hex(0, -1, +1), 
                          Hex(-1, 0, +1), Hex(-1, +1, 0), Hex(0, +1, -1)]

def cube_scale(hex: Hex, factor: int) -> Hex:
    return Hex(hex.q * factor, hex.r * factor, hex.s * factor)

def cube_direction(direction: int) -> Hex:
    return cube_direction_vectors[direction]

def cube_add(hex: Hex, vec: Hex) -> Hex:
    return Hex(hex.q + vec.q, hex.r + vec.r, hex.s + vec.s)

def cube_neighbor(cube: Hex, direction: int) -> Hex:
    return cube_add(cube, cube_direction(direction))

def cube_neighbors(center: Hex) -> [Hex]:
    return [cube_neighbor(center, i) for i in range(6)]

def num_black_neighbors(center: Hex, black: dict) -> int:
    return sum(int(black[tile]) for tile in cube_neighbors(center) if tile in black)

def cube_ring(center: Hex, radius: int) -> [Hex]:
    results = []
    hex = cube_add(center, cube_scale(cube_direction(4), radius))
    for i in range(6):
        for _ in range(radius):
            results.append(hex)
            hex = cube_neighbor(hex, i)
    return results

def perform_cell(hex: (int, int, int), black: dict) -> (bool, bool):
    count = num_black_neighbors(hex, black)
    if hex not in black or not black[hex]:
        if count == 2:
            return True, True
    elif count == 0 or count >= 3:
        return False, True
    return black[hex], False

def once(black: dict) -> dict:
    radius = 1
    copy = defaultdict(bool)
    center = Hex(0, 0, 0)
    seen = set()
    seen.add(center)
    copy[center] = perform_cell(center, black)[0]
    over = False
    while True:
        flipped_any = False
        for hex in cube_ring(center, radius):
            seen.add(hex)
            copy[hex], flipped = perform_cell(hex, black)
            flipped_any = flipped_any or flipped
        if over:
            break
        if not flipped_any and all(tile in seen for tile in black.keys() if black[tile]):
            over = True
        radius += 1
    return copy

def conway(black: dict, n: int = 100):
    for _ in range(n):
        black = once(black)
    return num_black(black)

lines = open(argv[1]).readlines()
black = defaultdict(bool)
for line in lines:
    walk(line.strip(), black)
print(num_black(black))
print(conway(black, 100))