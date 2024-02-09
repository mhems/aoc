from sys import argv
from collections import deque

def parse_line(line: str) -> (int, int):
    tokens = line.strip().split()
    return int(tokens[0]), int(tokens[-2])

def simulate(num_players: int, num_marbles: int) -> int:
    scores = [0] * num_players
    ring = deque()
    for i in range(num_marbles + 1):
        if i != 0 and i % 23 == 0:
            ring.rotate(7)
            scores[i % num_players] += i + ring.popleft()
        else:
            ring.rotate(-2)
            ring.appendleft(i)
    return max(scores)

with open(argv[1]) as fp:
    lines = fp.readlines()

pairs = [parse_line(line.strip()) for line in lines]
for num_players, num_marbles in pairs:
    print(simulate(num_players, num_marbles))
