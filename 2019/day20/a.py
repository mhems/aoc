from sys import argv
from collections import defaultdict
from collections import deque

lines = [list(line.rstrip()) for line in open(argv[1]).readlines()]

def parse() -> ([[str]], {str: [(int, int)]}):
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

def bfs(grid, start, end) -> int:
    q = deque([(start, 0)])
    visited = {start}
    while q:
        cur, d = q.popleft()
        visited.add(cur)
        if end == cur:
            return d
        for n in vacant_neighbors(grid, cur):
            if n not in visited:
                q.append((n, d + 1))
    return None

def condense(grid, portals, start, stop):
    H, W = len(grid), len(grid[0])
    def is_outer(pos):
        y, x = pos
        return y == 0 or y == H-1 or x == 0 or x == W-1
    nodes = {start: 'AA', stop: 'ZZ'}
    inners, outers = set(), set()
    adj_list = defaultdict(dict)
    for k, v in portals.items():
        for e in v:
            nodes[e] = k
        if len(v) > 1:
            inner, outer = sorted(v, key=lambda pos: int(is_outer(pos)))
            inners.add(inner)
            outers.add(outer)
        adj_list[f'outer-{k}'] = {f'inner-{k}': 1}
        adj_list[f'inner-{k}'] = {f'outer-{k}': 1}
    def qualify(label, pos):
        if pos in inners:
            return f'inner-{label}'
        else:
            return f'outer-{label}'
    for pos1, label1 in nodes.items():
        for pos2, label2 in nodes.items():
            if pos1 != pos2:
                d = bfs(grid, pos1, pos2)
                if d:
                    l1, l2 = qualify(label1, pos1), qualify(label2, pos2)
                    adj_list[l1][l2] = d
                    adj_list[l2][l1] = d
    return dict(adj_list)

grid, portals = parse()
start, stop = portals.pop('AA')[0], portals.pop('ZZ')[0]
reverse_map = reverse(portals)
print(portal_bfs(grid, reverse_map, start, stop))

adj_list = condense(grid, portals, start, stop)

def recursive_bfs(adj_list: dict[str, dict[str, int]]) -> int:
    q = deque([('outer-AA', 0, 0)])
    visited = set()
    while q:
        cur, depth, distance = q.popleft()
        key = cur, depth
        if key in visited:
            continue
        visited.add(key)
        if depth == 0 and cur == 'outer-ZZ':
            return distance
        cur_outer = cur.startswith('outer')
        for v, w in adj_list[cur].items():
            if depth != 0 and v == 'outer-ZZ':
                continue
            neighbor_outer = v.startswith('outer')
            if cur[-2:] == v[-2:]:
                if cur_outer and not neighbor_outer:
                    q.append((v, depth - 1, distance + 1))
                else:
                    q.append((v, depth + 1, distance + 1))
            else:
                if depth == 0 and neighbor_outer and v[-2:] != 'ZZ':
                    continue
                q.append((v, depth, distance + w))

def plot():
    import networkx as nx
    G = nx.Graph()
    for u, d in adj_list.items():
        for v, w in d.items():
            G.add_edge(u, v, weight=w)
    nx.drawing.nx_pydot.write_dot(G, argv[1].split('.')[0] + ".dot")
#plot()

print(recursive_bfs(adj_list))