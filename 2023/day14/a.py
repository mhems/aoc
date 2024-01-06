from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()
grid = [line.strip() for line in lines]

def gather_columns_as_rows(grid: [[str]]) -> [[str]]:
    R = len(grid)
    C = len(grid[0])
    return [''.join(grid[R-1-r][c] for r in range(R)) for c in range(C)]

def print_grid(grid: [[str]]):
    print('\n'.join(grid))

gp = gather_columns_as_rows(grid)

def compute_load(col: str) -> int:
    load = 0
    rock_count = 0
    for i, ch in enumerate(col):
        if ch == 'O':
            rock_count += 1
        elif ch == '#':
            load += sum(range(i + 1 - rock_count, i+1, 1))
            #print('ledge at', i+1, ', rocks:', rock_count, 'load:', load)
            rock_count = 0
    load += sum(range(i + 1 - rock_count + 1, i+2, 1))
    #print('rocks remain:', rock_count, 'load:', load)
    return load

for col in gp:
    #print(col)
    l = compute_load(col)
    #print(l)
answer = sum(compute_load(col) for col in gp)
print(answer)
