from sys import argv
from itertools import cycle

def play(p1: int, p2: int, goal: int = 1000, num_die_sides: int = 100, board_size: int = 10) -> int:
    ps = [p1 - 1, p2 - 1]
    scores = [0, 0]
    die = cycle(range(1, num_die_sides + 1))
    num_rolls = 0

    while True:
        for i in (0, 1):
            val = sum((next(die), next(die), next(die)))
            num_rolls += 3
            ps[i] = (ps[i] + val) % board_size
            scores[i] += ps[i] + 1
            if any(score >= goal for score in scores):
                return min(scores) * num_rolls

p1, p2 = [int(line.strip().split()[-1]) for line in open(argv[1]).readlines()]
print(play(p1, p2))
