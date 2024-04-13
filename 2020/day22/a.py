from sys import argv
from collections import deque

def parse() -> (deque, deque):
    a, b = open(argv[1]).read().strip().split('\n\n')
    def parse_player(text: str) -> deque:
        return deque(map(int, text.strip().split('\n')[1:]))
    return parse_player(a), parse_player(b)

def score(d: deque) -> int:
    return sum((len(d) - i) * e for i, e in enumerate(d))

def play_game(d1: deque, d2: deque, recurse: bool = False) -> (bool, int):
    history = set()
    round = 0
    while d1 and d2:
        t = tuple(d1)
        if t in history:
            return True, score(d1)
        history.add(t)
        a, b = d1.popleft(), d2.popleft()
        if recurse and len(d1) >= a and len(d2) >= b:
            sd1 = deque(d1)
            for _ in range(len(d1) - a):
                sd1.pop()
            sd2 = deque(d2)
            for _ in range(len(d2) - b):
                sd2.pop()
            p1_wins, _ = play_game(sd1, sd2, True)
            if p1_wins:
                d1.append(a)
                d1.append(b)
            else:
                d2.append(b)
                d2.append(a)
        elif a > b:
            d1.append(a)
            d1.append(b)
        elif b > a:
            d2.append(b)
            d2.append(a)
        round += 1
    if d1:
        return True, score(d1)
    return False, score(d2)

print(play_game(*parse())[1])
print(play_game(*parse(), True)[1])
