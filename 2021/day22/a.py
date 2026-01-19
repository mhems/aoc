from sys import argv
from math import prod

class Cuboid:
    def __init__(self, x, y, z, factor: int):
        self.min = x[0], y[0], z[0]
        self.max = x[1], y[1], z[1]
        self.factor = factor
    @property
    def volume(self) -> int:
        return self.factor * prod(b - a + 1 for a, b in zip(self.min, self.max))
    def intersect(self, other):
        mins, maxs = [0] * 3, [0] * 3
        intersect = True
        for i in range(3):
            mins[i] = max(self.min[i], other.min[i])
            maxs[i] = min(self.max[i], other.max[i])
            if mins[i] > maxs[i]:
                intersect = False
        if intersect:
            return Cuboid(*zip(mins, maxs), -self.factor)
        return None

class World:
    fifty = Cuboid((-50, 50), (-50, 50), (-50, 50), 1)
    def __init__(self):
        self.cuboids = []
    def num_on(self) -> tuple[int, int]:
        v1, v2 = 0, 0
        for cuboid in self.cuboids:
            intersection = cuboid.intersect(World.fifty)
            if intersection is not None:
                v1 += cuboid.factor * abs(intersection.volume)
            v2 += cuboid.volume
        return v1, v2
    def add_region(self, new):
        new_cuboids = []
        for cuboid in self.cuboids:
            intersection = cuboid.intersect(new)
            if intersection is not None:
                new_cuboids.append(intersection)
        if len(new_cuboids) > 0:
            self.cuboids.extend(new_cuboids)
        if new.factor == 1:
            self.cuboids.append(new)

def parse_step(text: str) -> Cuboid:
    return Cuboid(*[tuple(map(int, token[token.index('=') + 1:].split('..')))
                    for token in text[text.index('x'):].split(',')],
                  1 if text.startswith('on') else -1)

world = World()
for cuboid in [parse_step(line.strip()) for line in open(argv[1]).readlines()]:
    world.add_region(cuboid)
print('\n'.join(map(str, world.num_on())))
