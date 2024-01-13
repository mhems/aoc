from sys import argv
from collections import namedtuple as nt

Seq = nt('Seq', ['name', 'a', 'b'])

with open(argv[1]) as fp:
    lines = fp.readlines()

def parse_seq(text: str) -> Seq:
    tokens = text.split()
    if tokens[0] == 'rect':
        a, b = map(int, tokens[1].split('x'))
        return Seq('rect', a, b)
    return Seq(tokens[1], int(tokens[2].split('=')[1]), int(tokens[-1]))

def print_grid(grid: [[bool]]):
    print('\n'.join(''.join(map(lambda b: '#' if b else '.', row)) for row in grid))
    
def apply_seq(grid: [[bool]], seq: Seq):
    def rotate(s, n: int):
        return s[-n:] + s[:-n]
    if seq.name == 'rect':
        for x in range(seq.a):
            for y in range(seq.b):
                grid[y][x] = True
    elif seq.name == 'row':
        grid[seq.a] = rotate(grid[seq.a], seq.b)
    else:
        column = [line[seq.a] for line in grid]
        for i, cell in enumerate(rotate(column, seq.b)):
            grid[i][seq.a] = cell

def num_lit(grid: [[bool]]) -> int:
    return sum(sum(int(e) for e in row) for row in grid)

seqs = [parse_seq(line.strip()) for line in lines]
R, C = 6, 50 # 3, 7
grid = [[False] * C for _ in range(R)]

for seq in seqs:
    #print(seq)
    apply_seq(grid, seq)
    #print_grid(grid)
    #print()
print(num_lit(grid))
print_grid(grid)
