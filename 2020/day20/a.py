from sys import argv
from math import prod, sqrt
from collections import defaultdict
import re

def parse() -> {int: [str]}:
    def parse_tile(text: str) -> (int, [str]):
        lines = text.strip().split('\n')
        return int(lines[0][5:-1]), [line.strip() for line in lines[1:]]
    return dict(parse_tile(chunk) for chunk in open(argv[1]).read().split('\n\n'))

def top(grid: [str]) -> str:
    return grid[0]

def bottom(grid: [str]) -> str:
    return grid[-1]

def left(grid: [str]) -> str:
    return ''.join(row[0] for row in grid)

def right(grid: [str]) -> str:        
    return ''.join(row[-1] for row in grid)

def build_edge_map(tiles: {int: [str]}) -> {str: {int}}:
    edge_to_tiles = defaultdict(set)
    for id, tile in tiles.items():
      for func in (top, bottom, left, right):
          edge = func(tile)
          if edge[::-1] in edge_to_tiles:
              edge_to_tiles[edge[::-1]].add(id)
          else:
              edge_to_tiles[edge].add(id)
    return edge_to_tiles

def partition(tiles: {int: [str]}):
    corners, edges, inners = set(), set(), set()
    tallies = defaultdict(list)
    edge_to_tiles = build_edge_map(tiles)
    for ids in edge_to_tiles.values():
        if len(ids) > 1:
            for id in ids:
                tallies[id].append(next(iter(ids - {id})))
    for id, neighbors in tallies.items():
        if len(neighbors) == 2:
            corners.add(id)
        elif len(neighbors) == 3:
            edges.add(id)
        else:
            inners.add(id)
    return edge_to_tiles, tallies, corners, edges, inners

def rot90cw(grid: [str]) -> str:
    return [''.join(grid[row][col] for row in range(len(grid) - 1, -1, -1)) for col in range(len(grid[0]))]

def reverse(grid: [str]) -> str:
    return [''.join(reversed(row)) for row in grid]

def print_grid(grid):
    print('\n'.join(''.join(map(str, row)) for row in grid), end='\n\n')

def generate_orientations(grid: [str]):
    for _ in range(4):
        yield grid
        yield reverse(grid)
        grid = rot90cw(grid)

def arrange(tiles: {int: [str]}, # id to tile grid
            neighbors: {int: [int]}, # tile id to ids of neighboring tiles
            corners: {int}, # ids of 4 corners
            edges: {int}) -> [[int]]: # ids of 4*(n-2) edges
    N = int(sqrt(len(tiles)))
    grid = [[None] * N for _ in range(N)]
    
    def place_edge(pos: (int, int), previous: int, dy1: int, dx1: int, dy2: int, dx2: int):
        y, x = pos
        a, b = set(neighbors[grid[y][x]]) - {previous}
        grid[y+dy1][x+dx1], grid[y+dy2][x+dx2] = (a, b) if a in edges or a in corners else (b, a)            

    def place_inner(row: int, col: int):
        placed = {grid[row + dy][col + dx] for dy, dx in [(0, -1), (-1, 0), (0, 1)]}
        grid[row+1][col] = (set(neighbors[grid[row][col]]) - placed).pop()

    grid[0][0] = corners.pop()
    grid[0][1], grid[1][0] = neighbors[grid[0][0]]
    for i in range(1, N-1):
        place_edge((0, i), grid[0][i-1], 0, 1, 1, 0)
    grid[1][N-1] = (set(neighbors[grid[0][N-1]]) - {grid[0][N-1]} - {grid[0][N-2]}).pop()
    for i in range(1, N-1):
        place_edge((i, N-1), grid[i-1][N-1], 1, 0, 0, -1)
    grid[N-1][N-2] = (set(neighbors[grid[N-1][N-1]]) - {grid[N-1][N-1]} - {grid[N-2][N-1]}).pop()
    for i in range(1, N-1):
        place_edge((N-1, N-1-i), grid[N-1][N-1-i+1], 0, -1, -1, 0)
    grid[N-2][0] = (set(neighbors[grid[N-1][0]]) - {grid[N-1][0]} - {grid[N-1][1]}).pop()
    for i in range(1, N-2):
        place_edge((N-1-i, 0), grid[N-1-i+1][0], -1, 0, 0, 1)
    for row in range(1, N-3):
        for col in range(2, N-2):
            place_inner(row, col)
    return grid

def orient(grid: [[int]], tiles: {int: [str]}, edges_to_tiles: {str: {int}}) -> [str]:
    N = len(grid)
    oriented = [[None] * N for _ in range(N)]
    pair_to_edge = {}
    for edge, ids in edges_to_tiles.items():
        if len(ids) == 2:
            a, b = ids
            pair_to_edge[(a, b)] = edge
            pair_to_edge[(b, a)] = edge

    def orient_top_row(col: int) -> [str]:
        l = pair_to_edge[(grid[0][col], grid[0][col-1])]
        r = pair_to_edge[(grid[0][col], grid[0][col+1])]
        b = pair_to_edge[(grid[0][col], grid[1][col])]
        for orientation in generate_orientations(tiles[grid[0][col]]):
            lo = left(orientation)
            if lo == l or lo == l[::-1]:
                ro = right(orientation)
                if ro == r or ro == r[::-1]:
                    bo = bottom(orientation)
                    if bo == b or bo == b[::-1]:
                        return orientation
    
    def orient_right_col(row: int) -> [str]:
        t = pair_to_edge[(grid[row][N-1], grid[row-1][N-1])]
        l = pair_to_edge[(grid[row][N-1], grid[row][N-2])]
        b = pair_to_edge[(grid[row][N-1], grid[row+1][N-1])]
        for orientation in generate_orientations(tiles[grid[row][N-1]]):
            to = top(orientation)
            if to == t or to == t[::-1]:
                lo = left(orientation)
                if lo == l or lo == l[::-1]:
                    bo = bottom(orientation)
                    if bo == b or bo == b[::-1]:
                        return orientation
    
    def orient_bottom_row(col: int) -> [str]:
        l = pair_to_edge[(grid[N-1][col], grid[N-1][col-1])]
        r = pair_to_edge[(grid[N-1][col], grid[N-1][col+1])]
        t = pair_to_edge[(grid[N-1][col], grid[N-2][col])]
        for orientation in generate_orientations(tiles[grid[N-1][col]]):
            to = top(orientation)
            if to == t or to == t[::-1]:
                lo = left(orientation)
                if lo == l or lo == l[::-1]:
                    ro = right(orientation)
                    if ro == r or ro == r[::-1]:
                        return orientation
    
    def orient_left_col(row: int) -> [str]:
        t = pair_to_edge[(grid[row][0], grid[row-1][0])]
        r = pair_to_edge[(grid[row][0], grid[row][1])]
        b = pair_to_edge[(grid[row][0], grid[row+1][0])]
        for orientation in generate_orientations(tiles[grid[row][0]]):
            to = top(orientation)
            if to == t or to == t[::-1]:
                bo = bottom(orientation)
                if bo == b or bo == b[::-1]:
                    ro = right(orientation)
                    if ro == r or ro == r[::-1]:
                        return orientation

    def orient_top_left_corner() -> [str]:
        r = left(oriented[0][1])
        b = top(oriented[1][0])
        for orientation in generate_orientations(tiles[grid[0][0]]):
            ro = right(orientation)
            if ro == r or ro == r[::-1]:
                bo = bottom(orientation)
                if bo == b or bo == b[::-1]:
                    return orientation
    
    def orient_top_right_corner() -> [str]:
        l = right(oriented[0][N-2])
        b = top(oriented[1][N-1])
        for orientation in generate_orientations(tiles[grid[0][N-1]]):
            lo = left(orientation)
            if lo == l or lo == l[::-1]:
                bo = bottom(orientation)
                if bo == b or bo == b[::-1]:
                    return orientation
    
    def orient_bottom_left_corner() -> [str]:
        r = left(oriented[N-1][1])
        t = bottom(oriented[N-2][0])
        for orientation in generate_orientations(tiles[grid[N-1][0]]):
            ro = right(orientation)
            if ro == r or ro == r[::-1]:
                to = top(orientation)
                if to == t or to == t[::-1]:
                    return orientation
    
    def orient_bottom_right_corner() -> [str]:
        l = right(oriented[N-1][N-2])
        t = bottom(oriented[N-2][N-1])
        for orientation in generate_orientations(tiles[grid[N-1][N-1]]):
            lo = left(orientation)
            if lo == l or lo == l[::-1]:
                to = top(orientation)
                if to == t or to == t[::-1]:
                    return orientation

    def orient_inner(row: int, col: int) -> [str]:
        t = bottom(oriented[row-1][col])
        l = right(oriented[row][col-1])
        for orientation in generate_orientations(tiles[grid[row][col]]):
            lo = left(orientation)
            if lo == l or lo == l[::-1]:
                to = top(orientation)
                if to == t or to == t[::-1]:
                    return orientation

    for col in range(1, N-1):
        oriented[0][col] = orient_top_row(col)
    for row in range(1, N-1):
        oriented[row][N-1] = orient_right_col(row)
    for col in range(1, N-1):
        oriented[N-1][col] = orient_bottom_row(col)
    for row in range(1, N-1):
        oriented[row][0] = orient_left_col(row)
    oriented[0][0] = orient_top_left_corner()
    oriented[0][N-1] = orient_top_right_corner()
    oriented[N-1][0] = orient_bottom_left_corner()
    oriented[N-1][N-1] = orient_bottom_right_corner()
    for row in range(1, N-1):
        for col in range(1, N-1):
            oriented[row][col] = orient_inner(row, col)

    expanded = []
    for row in range(N):
        for i in range(1, 9):
            expanded.append(''.join(oriented[row][col][i][1:-1] for col in range(N)))
    return expanded

line1 = re.compile(r'..................#.')
line2 = re.compile(r'#....##....##....###')
line3 = re.compile(r'.#..#..#..#..#..#...')
def num_monsters(grid: [str]) -> int:
    num_monsters = 0
    for i in range(1, len(grid) - 1):
        match = re.search(line2, grid[i])
        if match is not None:
            j = match.start()
            while j + 20 < len(grid[i]):
                if re.match(line2, grid[i][j:]) and re.match(line1, grid[i-1][j:]) and re.match(line3, grid[i+1][j:]):
                    num_monsters += 1
                j += 1
    return num_monsters

def num_non_monster(grid: [str]) -> int:
    for orientation in generate_orientations(grid):
        n = num_monsters(orientation)
        if n > 0:
            return sum(row.count('#') for row in grid) - n * 15

tiles = parse()
edges_to_tiles, neighbors, corners, edges, _ = partition(tiles)
print(prod(corners))
arranged = arrange(tiles, neighbors, corners, edges)
oriented = orient(arranged, tiles, edges_to_tiles)
print(num_non_monster(oriented))
