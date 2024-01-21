from sys import argv
from math import sqrt

n = int(argv[1])

root = int(sqrt(n))
if root * root != n:
    root += 1
if root % 2 == 0:
    root += 1

def make_grid(n: int, size: int):
    def move(pos: (int, int), amt: (int, int)) -> (int, int):
        return (pos[0] + amt[0], pos[1] + amt[1]) 
    moves = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    pos = (size//2, size//2)
    v = 2
    step = 1
    dir_index = 0
    while v <= n:
        dir = moves[dir_index % len(moves)]
        for _ in range(step):
            pos = move(pos, dir)
            v += 1
            if v > n:
                return pos
        dir_index += 1
        
        dir = moves[dir_index % len(moves)]
        for _ in range(step):
            pos = move(pos, dir)
            v += 1
            if v > n:
                return pos
        dir_index += 1

        step += 1

pos = make_grid(n, root)
print(abs(pos[0] - root//2) + abs(pos[1] - root//2))
