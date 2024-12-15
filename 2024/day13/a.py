from sys import argv
from collections import namedtuple as nt
import numpy as np

Coord = nt('Coord', ['x', 'y'])
Machine = nt('Machine', ['a', 'b', 'prize'])

def parse_coord(text: str) -> Coord:
    x, y = text.strip().split()[-2:]
    i = 1 if text.startswith('Button') else 2
    return Coord(int(x.rstrip(',')[i:]), int(y[i:]))

def parse_machine(text: str) -> Machine:
    return Machine(*(parse_coord(line) for line in text.strip().split('\n')))

def achievable(machine: Machine, m: int, n: int) -> bool:
    return (machine.a.x * m + machine.b.x * n == machine.prize.x and
            machine.a.y * m + machine.b.y * n == machine.prize.y)

def cheapest_win(machine: Machine) -> int:
    a = np.array([[machine.a.x, machine.b.x], [machine.a.y, machine.b.y]])
    prize = np.array([[machine.prize.x], [machine.prize.y]])
    a_inv = np.linalg.inv(a)
    x = a_inv @ prize
    m, n = round(x[0][0]), round(x[1][0])
    if m >= 0 and n >= 0 and achievable(machine, m, n):
        return 3 * m + n
    return 0

machines = [parse_machine(machine) for machine in open(argv[1]).read().split('\n\n')]
print(sum(cheapest_win(machine) for machine in machines))
machines = [Machine(machine.a,
                    machine.b,
                    Coord(machine.prize.x + 10000000000000, machine.prize.y + 10000000000000))
            for machine in machines]
print(sum(cheapest_win(machine) for machine in machines))
