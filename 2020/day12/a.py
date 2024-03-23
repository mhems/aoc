from sys import argv

def manhattan(p1: (int, int), p2: (int, int) = None) -> int:
    if p2 is None:
        p2 = (0, 0)
    return sum(abs(a - b) for a, b in zip(p1, p2))

def travel(directions: [(str, int)]) -> int:
    x = y = 0
    dir = 1
    deltas = ((-1, 0), (0, 1), (1, 0), (0, -1))
    for op, val in directions:
        if op in 'NESW':
            dir = 'NESW'.index(op)
            dy, dx = deltas[dir]
            x += dx * val
            y += dy * val
        elif op in 'LR':
            if op == 'R':
                dir = (dir + val//90) % 4
            else:
                dir = (dir - val//90) % 4
        else:
            dy, dx = deltas[dir]
            x += dx * val
            y += dy * val
    return manhattan((y, x))

def waypoint(directions: [(str, int)]) -> int:
    x_ship = y_ship = 0
    y_way, x_way = (-1, 10)
    deltas = ((-1, 0), (0, 1), (1, 0), (0, -1))
    for op, val in directions:
        if op in 'NESW':
            dy, dx = deltas['NESW'.index(op)]
            x_way += dx * val
            y_way += dy * val
        elif op in 'LR':
            x_diff = x_way - x_ship
            y_diff = y_way - y_ship
            for _ in range(val//90):
                if op == 'L':
                    x_diff, y_diff = y_diff, -x_diff
                else:
                    x_diff, y_diff = -y_diff, x_diff
            x_way = x_ship + x_diff
            y_way = y_ship + y_diff
        else:
            x_diff = x_way - x_ship
            y_diff = y_way - y_ship
            x_ship += x_diff * val
            y_ship += y_diff * val
            x_way = x_ship + x_diff
            y_way = y_ship + y_diff
    return manhattan((y_ship, x_ship))

directions = [(line[0], int(line[1:].rstrip())) for line in open(argv[1]).readlines()]
print(travel(directions))
print(waypoint(directions))
