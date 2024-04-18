from sys import argv

def distance(a: (int, int), b: (int, int)) -> int:
    return tuple(i - j for i, j in zip(a, b))

def trace(directions: [(str, int)], num_tails: int = 1) -> int:
    deltas = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    def move(pos: (int, int), arg) -> (int, int):
        delta = deltas[arg] if isinstance(arg, str) else arg
        return tuple(a + b for a, b in zip(pos, delta))
    def move_tail(tail: (int, int), head: (int, int)) -> (int, int):
        dy, dx = distance(head, tail)
        if abs(dy) < 2 and abs(dx) < 2:
            return tail
        if dy != 0 and dx != 0:
            return move(tail, (dy//abs(dy), dx//abs(dx)))
        elif dy == 0:
            return move(tail, (0, dx//abs(dx)))
        elif dx == 0:    
            return move(tail, (dy//abs(dy), 0))
        assert False
    assert num_tails >= 1
    visited = set()
    h = (0, 0)
    tails = [tuple(h) for _ in range(num_tails)]
    visited.add(tails[-1])
    for dir, amt in directions:
        for _ in range(amt):
            h = move(h, dir)
            tails[0] = move_tail(tails[0], h)
            for i in range(1, len(tails)):
                tails[i] = move_tail(tails[i], tails[i-1])
            visited.add(tails[-1])
    return len(visited)

directions = [((t:= line.strip().split())[0], int(t[1])) for line in open(argv[1]).readlines()]
print(trace(directions))
print(trace(directions, 9))
