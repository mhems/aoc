from sys import argv
from tqdm import tqdm

with open(argv[1]) as fp:
    seeds = [int(line.strip()) for line in fp.readlines()]
factors = [16807, 48271]

def make_generator(seed: int, factor: int, multiple=None):
    cur = seed
    while True:
        cur = (cur * factor) % 2147483647
        if not multiple or cur % multiple == 0:
            yield cur

def simulate(ga, gb, n: int) -> int:
    match = 0
    for _ in tqdm(range(n)):
        a = next(ga)
        b = next(gb)
        match += int(a & 0xFFFF == b & 0xFFFF)
    return match

ga = make_generator(seeds[0], factors[0])
gb = make_generator(seeds[1], factors[1])
print(simulate(ga, gb, 40_000_000))

ga = make_generator(seeds[0], factors[0], 4)
gb = make_generator(seeds[1], factors[1], 8)
print(simulate(ga, gb, 5_000_000))