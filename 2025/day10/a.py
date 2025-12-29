import sys
import numpy as np
from itertools import chain, combinations

def power_set(items):
    return chain.from_iterable(combinations(items, r) for r in range(2, len(items)))

class Machine:
    def __init__(self, line: str):
        diagram, *schematics, requirements = line.rstrip().split()
        self.diagram = np.array([int(e == '#') for e in diagram[1:-1]])
        self.len = len(self.diagram)
        self.buttons = []
        N = np.count_nonzero(self.diagram)
        self.single = False
        for schematic in schematics:
            s = set(eval(schematic.replace(')', ',)')))
            button = np.array([int(i in s) for i in range(self.len)])
            if len(s) == N and np.array_equal(button, self.diagram):
                self.single = True
            self.buttons.append(button)
        self.levels = eval('[' + requirements[1:-1] + ']')
    def min_presses(self) -> int:
        if self.single:
            return 1
        for combo in power_set(self.buttons):
            if np.array_equal(sum(combo) % 2, self.diagram):
                return len(combo)

machines = [Machine(line) for line in open(sys.argv[1]).readlines()]
print(sum(machine.min_presses() for machine in machines))
