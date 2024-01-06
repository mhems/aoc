from sys import argv
from itertools import pairwise

with open(argv[1]) as fp:
    text = fp.read()

grids = [grid.strip().split('\n') for grid in text.strip().split('\n\n')]

def transpose(grid: [str]) -> [str]:
    R = len(grid)
    C = len(grid[0])
    return [''.join(grid[r][c] for r in range(R)) for c in range(C)]

def print_grid(grid: [str]):
    print('\n'.join(grid), end='\n\n')

def eval_candidate(row: int, grid: [str]) -> bool:
    cur_below = row
    cur_above = cur_below + 1
    found_smudge = False
    while cur_below >= 0 and cur_above < len(grid):
        equal = grid[cur_below] == grid[cur_above]
        if not equal:
            if found_smudge:
                return False
            elif difference(grid[cur_below], grid[cur_above]) == 1:
                found_smudge = True
        cur_below -= 1
        cur_above += 1
    return found_smudge

def difference(a: str, b: str) -> int:
    return sum(int(l1 != l2) for l1, l2 in zip(a, b))

def find_horz_reflection(grid: [str]) -> int:
    '''return number of rows above horizontal line of reflection, if one exists, otherwise -1'''
    mid = len(grid)//2
    indices = [i for i, pair in enumerate(pairwise(grid)) if difference(pair[0], pair[1]) < 2]
    #print(' ', indices)
    if len(indices) == 0:
        return -1
    sorted_indices = sorted(indices,
                            key=lambda i: abs(i - mid))
    for i in sorted_indices:
        if eval_candidate(i, grid):
            return i+1
    return -1

def find_reflection(grid: [str]) -> int:
    '''returns weighted reflection summary score'''
    #print('h')
    n = find_horz_reflection(grid)
    if n > 0:
        return n*100
    t_grid = transpose(grid)
    #print('v')
    n = find_horz_reflection(t_grid)
    return n

answer = 0
for i, grid in enumerate(grids):
    n = find_reflection(grid)
    if n < 0:
        print_grid(grid)

answer = sum(find_reflection(grid) for grid in grids)
print(answer)
