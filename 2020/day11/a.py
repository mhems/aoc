from sys import argv

def num_occupied(grid: [[str]], pos: (int, int)) -> int:
    num = 0
    u = l = r = d = False
    if pos[0] > 0:
        num += int('#' == grid[pos[0] - 1][pos[1]])
        u = True
    if pos[0] < len(grid) - 1:
        num += int('#' == grid[pos[0] + 1][pos[1]])
        d = True
    if pos[1] > 0:
        num += int('#' == grid[pos[0]][pos[1] - 1])
        l = True
    if pos[1] < len(grid[0]) - 1:
        num += int('#' == grid[pos[0]][pos[1] + 1])
        r = True
    if u and l:
        num += int('#' == grid[pos[0] - 1][pos[1] - 1])
    if u and r:
        num += int('#' == grid[pos[0] - 1][pos[1] + 1])
    if d and l:
        num += int('#' == grid[pos[0] + 1][pos[1] - 1])
    if d and r:
        num += int('#' == grid[pos[0] + 1][pos[1] + 1])
    return num

def num_visibly_occupied(grid: [[str]], pos: (int, int)) -> int:
    def seen_occupied_in_line(pos: (int, int), delta: (int, int)) -> bool:
        y, x = pos
        dy, dx = delta
        y += dy
        x += dx
        while 0 <= y < len(grid) and 0 <= x < len(grid[0]):
            if grid[y][x] == 'L':
                return False
            elif grid[y][x] == '#':
                return True
            y += dy
            x += dx
        return False
    deltas = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    return sum(int(seen_occupied_in_line(pos, delta)) for delta in deltas)

def count_occupied(grid: [[str]]) -> int:
    return sum(sum(int(c == '#') for c in row) for row in grid)

def once(grid: [[str]], func, threshold: int) -> [[str]]:
    new_grid = [[None] * len(grid[0]) for _ in range(len(grid))]
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            new_grid[y][x] = grid[y][x]
            if ch != '.':
                num = func(grid, (y, x))
                if ch == 'L' and num == 0:
                    new_grid[y][x] = '#'
                elif ch == '#' and num >= threshold:
                    new_grid[y][x] = 'L'
    return new_grid

def converge(grid: [[str]], part1=True) -> int:
    def state(grid: [[str]]) -> str:
        return ''.join(''.join(row) for row in grid)
    last = state(grid)
    threshold = 4 if part1 else 5
    func = num_occupied if part1 else num_visibly_occupied
    i = 0
    while True:
        grid = once(grid, func, threshold)
        s = state(grid)
        if s == last:
            return count_occupied(grid)
        last = s
        i += 1

grid = [list(line.strip()) for line in open(argv[1]).readlines()]
print(converge(grid))
print(converge(grid, False))
