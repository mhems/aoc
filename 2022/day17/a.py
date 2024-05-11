from sys import argv
from itertools import cycle, islice

def add(p1: (int, int), p2: (int, int)) -> (int, int):
    return tuple(a + b for a, b in zip(p1, p2))

def generate(start: (int, int), delta: (int, int), n: int):
    pos = start
    for _ in range(n):
        yield pos
        pos = add(pos, delta)

class Rock:
    def __init__(self, shape):
        self.is_uniform = isinstance(shape, tuple)
        if self.is_uniform:
            self.width, self.height = shape
            self.shape = [[True] * self.width for _ in range(self.height)]
        else:
            self.shape = shape
            self.width = len(shape[0])
            self.height = len(shape)
    def edge(self, pos: (int, int), dir: int) -> [(int, int)]:
        if dir == 0: # left
            if self.is_uniform:
                return [add(p, (0, 0)) for p in generate(pos, (1, 0), self.height)]
            elif self.shape[1][0]: # +
                return [add(pos, (0, 1)), add(pos, (1, 0)), add(pos, (2, 1))]
            return [add(pos, (0, 2)), add(pos, (1, 2)), add(pos, (2, 0))] # L
        elif dir == 1: # right
            if self.is_uniform or not self.shape[1][0]:
                return [add(p, (0, self.width - 1)) for p in generate(pos, (1, 0), self.height)]
            return [add(pos, (0, 1)), add(pos, (1, 2)), add(pos, (2, 1))] # +
        else: # down
            if self.is_uniform or not self.shape[1][0]:
                return [add(p, (self.height - 1, 0)) for p in generate(pos, (0, 1), self.width)]
            return [add(pos, (1, 0)), add(pos, (2, 1)), add(pos, (1, 2))] # +
    def move(self, chamber: [[bool]], pos: (int, int), dir: int) -> (int, int):
        deltas = [(0, -1), (0, 1), (1, 0)]
        ps = [add(p, deltas[dir]) for p in self.edge(pos, dir)]
        if any(not (0 <= x < len(chamber[0])) for _, x in ps):
            return pos
        if any(not (0 <= y < len(chamber)) for y, _ in ps):
            return pos
        return add(pos, deltas[dir]) if all(not chamber[p[0]][p[1]] for p in ps) else pos

def solidify(chamber: [[bool]], rock: Rock, pos: (int, int)):
    for y in range(rock.height):
        for x in range(rock.width):
            chamber[pos[0] + y][pos[1] + x] |= rock.shape[y][x]

def fall(rocks: [Rock], jets: [bool], n: int = 2022, width: int = 7) -> int:
    chamber = [[False] * width for _ in range(n * max(rock.height for rock in rocks))]
    y = len(chamber)
    jet_itr = cycle(jets)
    for rock in islice(cycle(rocks), n):
        pos = (y - rock.height - 3, 2)
        while True:
            j = next(jet_itr)
            new_pos = rock.move(chamber, pos, int(j))
            pos = new_pos
            #print('pos after sideways:', new_pos)
            new_pos = rock.move(chamber, pos, 2)
            #print('pos after down:', new_pos)
            if new_pos == pos:
                #print('HIT BOTTOM', pos)
                solidify(chamber, rock, pos)
                y = min(y, new_pos[0])
                #print_chamber(chamber)
                break
            pos = new_pos
    #print_chamber(chamber)
    return len(chamber) - y

def print_chamber(chamber: [[bool]]):
    for i, row in enumerate(chamber):
        if True in row:
            break
    for row in chamber[i:]:
        print(''.join('#' if cell else '.' for cell in row))
    print()

rocks = [Rock((4, 1)),
         Rock([[False, True, False],
                      [True, True, True],
                      [False, True, False]]),
         Rock([[False, False, True],
                      [False, False, True],
                      [True, True, True]]),
         Rock((1, 4)),
         Rock((2, 2))]
pushes = [l == '>' for l in open(argv[1]).read().strip()]
print(fall(rocks, pushes))
