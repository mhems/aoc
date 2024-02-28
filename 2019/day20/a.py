from sys import argv
from collections import defaultdict
from collections import deque

def parse() -> ([[str]], {str: [(int, int)]}):
    with open(argv[1]) as fp:
        lines = [list(line.rstrip()) for line in fp.readlines()]
    grid = []
    portals = defaultdict(list)
    for x, ch in enumerate(lines[0]):
        if ch != ' ':
            portal = ch + lines[1][x]
            portals[portal].append((0, x - 2))
    for i, line in enumerate(lines[2:]):
        if '#' not in line:
            for x, ch in enumerate(line):
                if ch != ' ':
                    portal = ch + lines[i+1+2][x]
                    portals[portal].append((i - 1, x - 2))
            return grid, dict(portals)
        if line[0] != ' ':
            portal = ''.join(line[:2])
            portals[portal].append((i, 0))
        if line[-1] != '#':
            portal = ''.join(line[-2:])
            portals[portal].append((i, len(line) - 3 - 2))
            line = line[:-2]
        for x in range(2, len(line)):
            if line[x].isalpha():
                if line[x+1].isalpha():
                    portal = ''.join(line[x:x+2])
                    portals[portal].append((i, x - 2 - 1 if line[x-1] == '.' else x + 2 - 2))
                    line[x] = ' '
                    line[x+1] = ' '
                elif lines[2 + i + 1][x].isalpha():
                    portal = line[x] + lines[i + 2 + 1][x]
                    portals[portal].append((i - 1 if lines[i-1+2][x] == '.' else i + 2, x - 2))
                    line[x] = ' '
                    lines[i+1+2][x] = ' '
        grid.append(line[2:])
        i += 1

def reverse(portals: {str: [(int, int)]}) -> {(int, int): (str, (int, int))}:
    reverse_map = {}
    for portal, positions in portals.items():
        p1, p2 = positions
        reverse_map[p1] = portal, p2
        reverse_map[p2] = portal, p1
    return reverse_map

def vacant_neighbors(grid: [[str]], pos: (int, int)) -> [(int, int)]:
    legal_positions = []
    if pos[0] > 0:
        legal_positions.append((pos[0] - 1, pos[1]))
    if pos[0] < len(grid) - 1:
        legal_positions.append((pos[0] + 1, pos[1]))
    if pos[1] > 0:
        legal_positions.append((pos[0], pos[1] - 1))
    if pos[1] < len(grid[0]) - 1:
        legal_positions.append((pos[0], pos[1] + 1))
    return [(y, x) for y, x in legal_positions if grid[y][x] == '.']

def portal_bfs(grid: [[str]],
               portals: {(int, int): (str, (int, int))},
               start: (int, int),
               end: (int, int)) -> int:
    q = deque()
    visited = set()
    q.append((start, tuple(), 0))
    visited.add((start, tuple()))
    while len(q) > 0:
        pos, portals_taken, steps = q.popleft()
        if pos == end:
            return steps
        for neighbor in vacant_neighbors(grid, pos):
            state = neighbor, portals_taken
            if state not in visited:
                visited.add(state)
                q.append((neighbor, portals_taken, steps + 1))
        if pos in portals:
            portal, other = portals[pos]
            if portal not in portals_taken:
                portals_taken = tuple([portal] + list(portals_taken))
                state = other, portals_taken
                if state not in visited:
                    visited.add(state)
                    visited.add((portal, portals_taken))
                    q.append((other, portals_taken, steps + 1))

grid, portals = parse()
start, stop = portals.pop('AA')[0], portals.pop('ZZ')[0]
reverse_map = reverse(portals)
print(portal_bfs(grid, reverse_map, start, stop))