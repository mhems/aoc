from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

class Vector:
    def __init__(self, text: str):
        self.x, self.y, self.z = map(int, text[3:-1].split(','))

    def add(self, v):
        self.x += v.x
        self.y += v.y
        self.z += v.z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

class Particle:
    def __init__(self, text: str):
        tokens = text.strip().split(', ')
        self.pos = Vector(tokens[0])
        self.vel = Vector(tokens[1])
        self.acc = Vector(tokens[2])

    def step(self):
        self.vel.add(self.acc)
        self.pos.add(self.vel)

def simulate(particles: [Particle]) -> int:
    i = 0
    while i < 1_000:
        remove = set()
        for a, particle in enumerate(particles):
            for b, other in enumerate(particles):
                if a != b and particle.pos == other.pos:
                    remove.add(a)
                    remove.add(b)
        if len(remove) > 0:
            i = 0
            for index in sorted(remove, reverse=True):
                particles.pop(index)
        for particle in particles:
            particle.step()
        i += 1
    return len(particles)

particles = [Particle(line.strip()) for line in lines]
print(simulate(particles))
