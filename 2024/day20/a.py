from sys import argv
from collections import deque
from tqdm import tqdm

def build_gridmap(grid: [str]) -> ((int, int), (int, int), {(int, int)}, {(int, int)}):
    start = None
    end = None
    walls = set()
    path = set()
    Y, X = len(grid), len(grid[0])
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '#':
                if 0 < y < Y - 1 and 0 < x < X - 1:
                    walls.add((y, x))
            else:
                if cell == 'S':
                    start = (y, x)
                elif cell == 'E':
                    end = (y, x)
                path.add((y, x))
    return start, end, walls, path

def neighbors(pos: (int, int)) -> {(int, int)}:
    return {(pos[0] + dy, pos[1] + dx) for dy, dx in [(-1, 0), (0, -1), (0, 1), (1, 0)]}

def bfs(open, start: (int, int), end: (int, int)) -> int:
    q = deque()
    visited = set([start])
    q.append(start)
    track = []
    while q:
        pos = q.popleft()
        track.append(pos)
        if pos == end:
            return track
        for n in neighbors(pos):    
            if n in open and n not in visited:
                visited.add(n)
                q.append(n)

def find_cheats(track, n) -> int:
    N = len(track)
    exit = N - n
    part1, part2 = 0, 0
    for i, u in tqdm(enumerate(track), total=exit):
        if i > exit:
            break
        j = i+n
        track_dist = 0
        while j < N:
            v = track[j]
            manhattan_dist = abs(v[0] - u[0]) + abs(v[1] - u[1])
            if track_dist >= manhattan_dist:
                if manhattan_dist <= 20:
                    part2 += 1
                    if manhattan_dist <= 2:
                        part1 += 1
            j += 1
            track_dist += 1
    return part1, part2

grid = [line.strip() for line in open(argv[1]).readlines()]
start, end, _, open = build_gridmap(grid)
track = bfs(open, start, end)
print(find_cheats(track, 50 if argv[1][0] == 'e' else 100))
