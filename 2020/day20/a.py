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
            assert len(ids) == 2
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
    return [''.join(grid[row][col] for row in range(len(grid) - 1, -1, -1))
            for col in range(len(grid[0]))]

def reverse(grid: [str]) -> str:
    return [''.join(reversed(row)) for row in grid]

def print_grid(grid):
    for row in grid:
        print(' '.join(map(str, row)))
    print()

def generate_orientations(grid: [str]):
    for _ in range(4):
        yield grid
        yield reverse(grid)
        grid = rot90cw(grid)

def arrange(tiles: {int: [str]},
            edges_to_tiles: {str: {int}},
            neighbors: {int: [int]},
            corners: {int},
            edges: {int},
            inners: {int}) -> [str]:
    '''arrange tiles returning stitched grid with seams removed'''
    N = int(sqrt(len(tiles)))
    pair_to_edge = {}
    for edge, ids in edges_to_tiles.items():
        if len(ids) == 2:
            a, b = ids.pop(), ids.pop()
            pair_to_edge[(a, b)] = edge
            pair_to_edge[(b, a)] = edge
    grid = [[None] * N for _ in range(N)]
    first_corner = corners.pop()
    right_neighbor = neighbors[first_corner][0]
    bottom_neighbor = neighbors[first_corner][1]
    right_edge = pair_to_edge[(first_corner, right_neighbor)]
    bottom_edge = pair_to_edge[(first_corner, bottom_neighbor)]
    for orientation in generate_orientations(tiles[first_corner]):
        print(right(orientation), right_edge, bottom(orientation), bottom_edge)
        if right(orientation) == right_edge and bottom(orientation) == bottom_edge:
            print_grid(orientation)
    #print_grid(grid)

line1 = re.compile(r'..................#.')
line2 = re.compile(r'#....##....##....###')
line3 = re.compile(r'.#..#..#..#..#..#...')
def num_monsters(grid: [str]) -> int:
    num_monsters = 0
    for i in range(1, len(grid) - 1):
        for match in re.finditer(line2, grid[i]):
            start = match.start()
            if re.match(line1, grid[i-1][start:]) and re.match(line3, grid[i+1][start:]):
                num_monsters += 1
    return num_monsters

def num_non_monster(grid: [str]) -> int:
    for orientation in generate_orientations(grid):
        n = num_monsters(orientation)
        if n > 0:
            return sum(row.count('#') for row in grid) - n * 15

tiles = parse()
edges_to_tiles, neighbors, corners, edges, inners = partition(tiles)
print(prod(corners))
grid = arrange(tiles, edges_to_tiles, neighbors, corners, edges, inners)
#print(num_non_monster(grid))