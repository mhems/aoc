from sys import argv

def print_grid(grid: [[str]]):
    print('\n'.join(''.join(row) for row in grid), end='\n\n')

def print_energized(grid: [[str]], energized: {(int, int)}):
    for y, row in enumerate(grid):
        for x in range(len(row)):
            print('#' if (y, x) in energized else '.', end='')
        print()
    print()

def trace_ray(grid: [[str]], pos: (int, int), dir: int) -> {(int, int)}:
    def trace_ray_inner(grid: [[str]], pos: (int, int), dir: int, done: ((int, int), int)) -> {(int, int)}:
        def in_bounds(pos: (int, int)) -> bool:
            return 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0])
        def apply_delta(pos: (int, int), dir: int) -> (int, int):
            deltas = ((-1, 0), (0, 1), (1, 0), (0, -1))
            return tuple(a + b for a, b in zip(pos, deltas[dir]))
        energized = set()
        if (pos, dir) in done:
            return energized
        done.add((pos, dir))
        by_dir = set()
        while in_bounds(pos):
            if (pos, dir) in by_dir:
                break
            val = grid[pos[0]][pos[1]]
            energized.add(pos)
            by_dir.add((pos, dir))
            if val == '|':
                if dir in (1, 3):
                    energized = energized.union(trace_ray_inner(grid, (pos[0] - 1, pos[1]), 0, done))
                    energized = energized.union(trace_ray_inner(grid, (pos[0] + 1, pos[1]), 2, done))
                    break
            elif val == '-':
                if dir in (0, 2):
                    energized = energized.union(trace_ray_inner(grid, (pos[0], pos[1] - 1), 3, done))
                    energized = energized.union(trace_ray_inner(grid, (pos[0], pos[1] + 1), 1, done))
                    break
            elif val == '/':
                change = {0: 1, 1: 0, 2: 3, 3: 2}
                dir = change[dir]
            elif val == '\\':
                change = {0: 3, 1: 2, 2: 1, 3: 0}
                dir = change[dir]
            pos = apply_delta(pos, dir)
        return energized
    energized = trace_ray_inner(grid, pos, dir, set())
    #print('pos=', pos, 'dir=', dir, 'num=', len(energized))
    #print_energized(grid, energized)
    return len(energized)

def find_best_entry(grid: [[str]]) -> int:
    best = 0
    for y in range(len(grid)):
        energized = trace_ray(grid, (y, 0), 1)
        best = max(best, energized)
        energized = trace_ray(grid, (y, len(grid[0]) - 1), 3)
        best = max(best, energized)
    for x in range(len(grid[0])):
        energized = trace_ray(grid, (0, x), 2)
        best = max(best, energized)
        energized = trace_ray(grid, (len(grid) - 1, x), 0)
        best = max(best, energized)
    return best

with open(argv[1]) as fp:
    grid = [list(line.strip()) for line in fp.readlines()]
print(trace_ray(grid, (0, 0), 1))
print(find_best_entry(grid))
