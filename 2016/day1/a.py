from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

paths = [[(t[0], int(t[1:])) for t in line.strip().split(', ')] for line in lines]

def walk_path(path: [(str, int)], part2: bool = False) -> int:
    cur = (0, 0)
    dir = 0
    seen = set(cur)
    def move(vector: (int, int), pos: (int, int), num: int) -> (int, int):
        for _ in range(num):
            pos = (pos[0] + vector[0], pos[1] + vector[1])
            if part2 and pos in seen:
                raise ValueError(str(abs(pos[0]) + abs(pos[1])))
            seen.add(pos)
        return pos
    try:
        for face, num in path:
            if dir == 0:
                if face == 'R':
                    dir = 2
                    cur = move((1, 0), cur, num)
                else:
                    dir = 3
                    cur = move((-1, 0), cur, num)
            elif dir == 1:
                if face == 'R':
                    dir = 3
                    cur = move((-1, 0), cur, num)
                else:
                    dir = 2
                    cur = move((1, 0), cur, num)
            elif dir == 2:
                if face == 'R':
                    dir = 1
                    cur = move((0, 1), cur, num)
                else:
                    dir = 0
                    cur = move((0, -1), cur, num)
            else:
                if face == 'R':
                    dir = 0
                    cur = move((0, -1), cur, num)
                else:
                    dir = 1
                    cur = move((0, 1), cur, num)
    except ValueError as e:
        return int(e.args[0])
    return abs(cur[0]) + abs(cur[1])

for path in paths:
    print(walk_path(path))
print()
for path in paths:
    print(walk_path(path, True))
