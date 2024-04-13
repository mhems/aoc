from sys import argv
from collections import namedtuple as nt
import numpy as np

Range = nt('Range', ['start', 'end'])
Step = nt('Step', ['on', 'x', 'y', 'z'])

def parse_range(text: str) -> Range:
    first_dot = text.index('.')
    start = int(text[:first_dot])
    end = int(text[first_dot + 2:])
    return Range(start, end)

def parse_step(text: str) -> Step:
    return Step(text.startswith('on'),
                *[parse_range(token[token.index('=') + 1:])
                 for token in text[text.index('x'):].split(',')])

def reboot(steps: [Step], n: int = 50) -> np.ndarray:
    grid = np.ndarray((2*n + 1, 2*n + 1, 2*n + 1), dtype=np.dtype(bool))
    grid.fill(False)
    for step in steps:
        sub = grid[(step.x.start + n): (step.x.end + n + 1),
                   (step.y.start + n): (step.y.end + n + 1),
                   (step.z.start + n): (step.z.end + n + 1)]
        sub.fill(step.on)
    return grid

def num_on(grid: np.ndarray) -> int:
    return grid.sum()

steps = [parse_step(line.strip()) for line in open(argv[1]).readlines()]
print(num_on(reboot(steps)))