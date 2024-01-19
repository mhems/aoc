from sys import argv
from tqdm import tqdm

with open(argv[1]) as fp:
    start = fp.read().strip()
R = int(argv[2])

def pos(row: str, i: int) -> bool:
    '''returns True if pos i is safe in next row'''
    safes = [ch == '.' for ch in row]
    safes = [True] + safes + [True]
    left, right, center = safes[i], safes[i+2], safes[i+1]
    if not left and not center and right:
        return False
    if not center and not right and left:
        return False
    if not left and center and right:
        return False
    if not right and center and left:
        return False
    return True

def next_row(row: str) -> str:
    return ''.join('.' if pos(row, i) else '^' for i in range(len(row)))

def generate(start: str, n: int) -> int:
    def num_safe(row: str) -> int:
        return sum(int(e == '.') for e in row)
    row = start
    total = num_safe(start)
    for _ in tqdm(range(n - 1)):
        row = next_row(row)
        total += num_safe(row)
    return total

print(generate(start, R))
