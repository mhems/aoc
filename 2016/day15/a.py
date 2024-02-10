from sys import argv

class Disc:
    def __init__(self, size: int, pos: int):
        self.size = size
        self.pos = pos

    def clone(self):
        return Disc(self.size, self.pos)

    def inc(self, amount: int = 1):
        self.pos = (self.pos + amount) % self.size
    
    def at_zero(self) -> bool:
        return self.pos == 0
    
    def __str__(self) -> str:
        return "%d/%d" % (self.pos, self.size)

def parse_line(line: str) -> Disc:
    tokens = line.strip().split()
    return Disc(int(tokens[3]), int(tokens[-1][:-1]))

def fall(discs: [Disc], time = 0) -> bool:
    discs = [disc.clone() for disc in discs]
    for disc in discs:
        disc.inc(time + 1)
    for i, disc in enumerate(discs):
        if not disc.at_zero():
            return False
        for disc in discs:
            disc.inc()
    return True

def find(discs: [Disc]) -> int:
    i = 0
    while True:
        if fall(discs, i):
            return i
        i += 1

with open(argv[1]) as fp:
    lines = fp.readlines()

discs = [parse_line(line.strip()) for line in lines]
print(find(discs))
discs.append(Disc(11, 0))
print(find(discs))