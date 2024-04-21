from sys import argv
from collections import deque

def mix(file: [int], n: int = 1) -> [int]:
    q = deque((i, e) for i, e in enumerate(file))
    for _ in range(n):
        for i in range(len(q)):
            while q[0][0] != i:
                q.rotate()
            j, v = q.popleft()
            q.rotate(-v % len(q))
            q.appendleft((j, v))
            q.rotate(v % len(q))
    return [v for _, v in q]

def grove_coordinates(file: [int]) -> [int]:
    loc = file.index(0)
    return [file[(loc + i) % len(file)] for i in (1000, 2000, 3000)]

def decrypt(file: [int], n: int = 1, key: int = 1) -> [int]:
    return sum(grove_coordinates(mix([key * e for e in file], n)))

file = [int(line.strip()) for line in open(argv[1]).readlines()]
print(decrypt(file))
print(decrypt(file, 10, 811589153))
