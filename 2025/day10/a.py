import sys
import numpy as np
from itertools import chain, combinations
import pulp
import sympy as sp

def power_set(items):
    return chain.from_iterable(combinations(items, r) for r in range(2, len(items)))

def make_vars(num):
    return [pulp.LpVariable(chr(i), lowBound=0, cat="Integer") for i in range(ord('a'), ord('a') + num)]

class Machine:
    def __init__(self, line: str):
        diagram, *schematics, requirements = line.rstrip().split()
        self.diagram = np.array([int(e == '#') for e in diagram[1:-1]])
        self.buttons = []
        N = np.count_nonzero(self.diagram)
        self.single = False
        for schematic in schematics:
            s = set(eval(schematic.replace(')', ',)')))
            button = np.array([int(i in s) for i in range(len(self.diagram))])
            if len(s) == N and np.array_equal(button, self.diagram):
                self.single = True
            self.buttons.append(button)
        self.button_matrix = np.vstack(self.buttons)
        self.levels = np.array(eval('[' + requirements[1:-1] + ']'))
    def min_presses(self) -> int:
        if self.single:
            return 1
        for combo in power_set(self.buttons):
            if np.array_equal(sum(combo) % 2, self.diagram):
                return len(combo)
    def min_levels(self):
        augmented = sp.Matrix(np.column_stack((self.button_matrix.transpose(), self.levels.transpose())))
        rref, _ = augmented.rref()
        variables = make_vars(len(self.buttons))
        prob = pulp.LpProblem("", pulp.LpMinimize)
        prob += sum(variables)
        for i in range(rref.rows):
            expr = 0
            for j in range(len(variables)):
                expr += rref[i, j] * variables[j]
            prob += expr == rref[i, len(variables)]
        prob.solve(pulp.PULP_CBC_CMD(msg=False))
        return int(pulp.value(prob.objective))

machines = [Machine(line) for line in open(sys.argv[1]).readlines()]
print(sum(machine.min_presses() for machine in machines))
print(sum(machine.min_levels() for machine in machines))
