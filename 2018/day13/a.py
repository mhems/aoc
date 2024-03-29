from sys import argv
from itertools import permutations

class Car:
    deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __init__(self, i: int, pos: (int, int), dir: int):
        self.i = i
        self.pos = pos
        self.dir = dir
        self.turn = 0
    
    def move(self, grid: [str]):
        self.pos = (self.pos[0] + Car.deltas[self.dir][0], self.pos[1] + Car.deltas[self.dir][1])
        ch = grid[self.pos[0]][self.pos[1]]
        if ch == '/':
            self.dir = ((self.dir + 1) % 2) + 2 * (self.dir // 2)
        elif ch == '\\':
            self.dir = 3 - self.dir
        elif ch == '+':
            if self.turn % 3 == 0:
                self.dir = (self.dir - 1) % 4
            elif self.turn % 3 == 2:
                self.dir = (self.dir + 1) % 4
            self.turn += 1

def find_cars(grid: [str]) -> [Car]:
    cars = []
    i = 0
    for y, line in enumerate(grid):
        for x, ch in enumerate(line):
            if ch in ('<', '>', '^', 'v'):
                cars.append(Car(i, (y, x), '^>v<'.index(ch)))
                i += 1
        grid[y] = grid[y].replace('<', '-').replace('>', '-').replace('^', '|').replace('v', '|')
    return cars

def tick(grid: [str], cars: [Car], prevent: bool = False):
    for car in sorted(cars, key=lambda car: car.pos):
        if car not in cars:
            continue
        original = car.pos
        car.move(grid)
        if prevent:
            to_remove = set()
            to_remove.add(car)
            for car2 in cars:
                if car2.pos in (original, car.pos):
                    to_remove.add(car2)
            if len(to_remove) > 1:
                for removal in to_remove:
                    cars.remove(removal)
    if not prevent:
        return set(c1.pos for c1, c2 in permutations(cars, 2) if c1.pos == c2.pos)

def simulate1(grid: [str], cars: [Car]) -> ((int, int), int):
    num_ticks = 0
    while True:
        for collision in tick(grid, cars):
            return (collision, num_ticks)
        num_ticks += 1

def simulate2(grid: [str], cars: [Car]) -> ((int, int), int):
    num_ticks = 0
    while True:
        tick(grid, cars, True)
        if len(cars) == 1:
            return (cars[0].pos, num_ticks)
        num_ticks += 1

with open(argv[1]) as fp:
    grid = [line.rstrip() for line in fp.readlines()]

cars = find_cars(grid)
print(simulate1(grid, cars))
print(simulate2(grid, cars))
