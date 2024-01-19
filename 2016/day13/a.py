from sys import argv

magic = int(argv[1])
x, y = map(int, argv[2:4])

def populate(x: int, y: int, magic: int) -> bool:
    '''return True iff (x, y) is open'''
    a = x*x + 3*x + 2*x*y + y + y*y + magic
    return bin(a)[2:].count('1') % 2 == 0

def make_grid(magic: int, X: int, Y: int) -> [[bool]]:
    grid = [[False] * X for _ in range(Y)]
    for y in range(Y):
        for x in range(X):
            grid[y][x] = populate(x, y, magic)
    grid.insert(0, [False] * X)
    grid.append([False] * X)
    for i, row in enumerate(grid):
        grid[i] = [False] + row + [False]
    return grid

def print_grid(grid: [[bool]], path=None):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if path is not None and (x, y) in path:
                print('O', end='')
            elif grid[y][x]:
                print('.', end='')
            else:
                print('#', end='')
        print()

def neighbors(grid: [[bool]], x: int, y: int) -> [(int, int)]:
    poses = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    neighbors = []
    for pos in poses:
        if grid[pos[1]][pos[0]]:
            neighbors.append(pos)
    return neighbors
            
def make_graph(grid: [[bool]]) -> {(int, int): [(int, int)]}:
    vertices = {}
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
            if grid[y][x]:
                ns = neighbors(grid, x, y)
                if len(ns) > 0:
                    vertices[(x, y)] = ns
    return vertices

def path(prev: {(int, int): [(int, int)]},
         src: (int, int),
         dst: (int, int)) -> [(int, int)]:
    S = []
    u = dst
    if prev[u] is not None or u == src:
        while u is not None:
            S.insert(0, u)
            u = prev[u]
    return S

def dijkstra(vertices: {(int, int): [(int, int)]},
             src: (int, int),
             dst: (int, int)) -> int:
    dist = {}
    prev = {}
    Q = []
    for vertex in vertices.keys():
        dist[vertex] = 2 ** 32
        prev[vertex] = None
        Q.append(vertex)
    dist[src] = 0
    while len(Q) > 0:
        u = min(((vertex, dist[vertex]) for vertex in Q),
                key=lambda pair: pair[1])[0]
        if u == dst:
            return len(path(prev, src, dst))
        Q.remove(u)
        for neighbor in vertices[u]:
            if neighbor in Q:
                alt = dist[u] + 1
                if alt < dist[neighbor]:
                    dist[neighbor] = alt
                    prev[neighbor] = u
    return None

def dfs(vertices: {(int, int): [(int, int)]},
        src: (int, int),
        dst: (int, int),
        discovered: {(int, int): bool} = None) -> int:
    if discovered is None:
        discovered = {}
    discovered[src] = True
    if src == dst:
        return (True, [])
    for neighbor in vertices[src]:
        if neighbor not in discovered:
            exists, path = dfs(vertices, neighbor, dst, discovered)
            if exists:
                #print(neighbor)
                return (True, path + [neighbor])
    return (False, -1)

def bfs(vertices: {(int, int): [(int, int)]},
        start: (int, int),
        limit: int,
        reachable: {(int, int)},
        n: int = 0):
    if reachable is None:
        reachable = set()
    if n <= limit:
        reachable.add(start)
        for neighbor in vertices[start]:
            bfs(vertices, neighbor, limit, reachable, n + 1)

grid = make_grid(magic, 30 * (x // 10 + 1), 30 * (y // 10 + 1))
print(len(grid[0]), len(grid))
#print_grid(grid, [(x, y)])
graph = make_graph(grid)
#print('\n'.join(map(str, graph.items())))
src, dst = (1+1, 1+1), (x+1, y+1)
print(dijkstra(graph, src, dst) - 1)
reachable = set()
bfs(graph, src, 50, reachable)
print(len(reachable))
