from sys import argv
from itertools import combinations
from math import lcm
import re

regex = r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>'

class Planet:
    def __init__(self, line):
        self.pos = [int(m) for m in re.match(regex, line.strip()).groups()]
        self.vel = [0, 0, 0]
    
    def gravity(self, other):
        for i in range(3):
            delta = self.pos[i] - other.pos[i]
            if delta > 0:
                self.vel[i] -= 1
                other.vel[i] += 1
            elif delta < 0:
                self.vel[i] += 1
                other.vel[i] -= 1

    def move(self):
        for i in range(3):
            self.pos[i] += self.vel[i]
            
    def state(self) -> (int, int, int, int, int, int):
        return tuple(self.pos + self.vel)

    def potential_energy(self) -> int:
        return sum(map(abs, self.pos))
    
    def kinetic_energy(self) -> int:
        return sum(map(abs, self.vel))

    def total_energy(self) -> int:
        return self.potential_energy() * self.kinetic_energy()

def simulate(planets: [Planet], n: int):
    def by_axis():
        return [[planet.pos[i] for planet in planets] for i in range(3)]
    init_pos_by_axis = by_axis()
    axis_cycle_lengths = [0] * 3
    i = 0
    while True:
        for a, b in combinations(planets, 2):
            a.gravity(b)
        for planet in planets:
            planet.move()
        i += 1

        if i == n:
            print(sum(planet.total_energy() for planet in planets))
            
        for axis, (init_axis_pos, axis_pos) in enumerate(zip(init_pos_by_axis, by_axis())):
            if axis_cycle_lengths[axis] == 0 and axis_pos == init_axis_pos:
                axis_cycle_lengths[axis] = i + 1
                if all(axis > 0 for axis in axis_cycle_lengths):
                    print(lcm(*axis_cycle_lengths))
                    return

planets = [Planet(line.strip()) for line in open(argv[1]).readlines()]
n = int(argv[2])
simulate(planets, n)
