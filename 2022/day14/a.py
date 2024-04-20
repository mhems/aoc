from sys import argv

def parse(paths: [str]) -> [[str]]:
    def parse_path(path: str) -> [((int, int), (int, int))]:
        pairs = eval('(' + path.strip().replace(' -> ', '),(') + ')')
        return [(pairs[i-1], pairs[i]) for i in range(1, len(pairs))]
    points = set()
    xs = set()
    ys = set()
    for path in paths:
        for line in parse_path(path):
            (x1, y1), (x2, y2) = line
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    points.add((y, x1))
                    ys.add(y)
                xs.add(x1)
            elif y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    points.add((y1, x))
                    xs.add(x)
                ys.add(y1)
            else:
                assert False
    xs.add(500)
    ys.add(0)
    points.add((0, 500))
    minX, maxX, maxY = min(xs), max(xs), max(ys)
    w = maxX + 1 - minX
    grid = [['.'] * (maxX + 50) for _ in range(maxY + 1)]
    for y, x in points:
        grid[y][x] = '#'
    return grid

def print_grid(grid: [[str]]):
    print('\n'.join(''.join(row) for row in grid))

def is_air(grid: [[str]], pos: (int, int)) -> bool:
    return grid[pos[0]][pos[1]] == '.'

def drop(grid: [[str]], pos: (int, int)):
    if pos[1] < 0 or pos[1] >= len(grid[0]) or pos[0] >= len(grid):
        return False
    y, x = pos
    while y < len(grid) and is_air(grid, (y, x)):
        y += 1
    if y >= len(grid):
        return False
    if is_air(grid, (y, x - 1)):
        return drop(grid, (y, x - 1))
    elif is_air(grid, (y, x + 1)):
        return drop(grid, (y, x + 1))
    elif is_air(grid, (y - 1, x)):
        grid[y - 1][x] = 'o'
        return True

def flow(grid: [[str]]) -> int:
    x = grid[0].index('#')
    grid[0][x] = '.'
    count = 0
    while is_air(grid, (0, x)):
        if not drop(grid, (0, x)):
            break
        count += 1
    return count

grid = parse(open(argv[1]).readlines())
#print_grid(grid)
print(flow(grid))

grid = parse(open(argv[1]).readlines())
grid.append(['.'] * len(grid[0]))
grid.append(['#'] * len(grid[0]))
print(flow(grid))
#print_grid(grid)
