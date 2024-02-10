from sys import argv
from hashlib import md5
from itertools import compress
from collections import deque

def hash(msg: str) -> str:
    return md5(bytes(msg, 'utf-8')).hexdigest().lower()

def available(path: str, pos: (int, int)) -> [(int, int)]:
    u, d, l, r = [a and b for a, b in zip(
        (ord(ch) > ord('a') for ch in hash(path)[:4]),
        (pos[1] > 0, pos[1] < 3, pos[0] > 0, pos[0] < 3))]
    deltas = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    return list(compress(((i, (pos[0] + d[0], pos[1] + d[1]))
                         for i, d in enumerate(deltas)),
                        (u, d, l, r)))

def bfs(path: str, pos: (int, int), paths: [str]):
    q = deque()
    q.append((path, pos))
    while len(q) > 0:
        cur_path, cur_pos = q.popleft()
        if cur_pos == (3, 3):
            paths.append(cur_path)
        else:
            for option in available(cur_path, cur_pos):
                q.append((cur_path + 'UDLR'[option[0]], option[1]))

passcode = argv[1]
paths = []
bfs(passcode, (0, 0), paths)
print(min(paths, key=len)[len(passcode):])
print(max(map(len, paths)) - len(passcode))
