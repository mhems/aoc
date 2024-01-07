from sys import argv
from itertools import pairwise

with open(argv[1]) as fp:
    lines = fp.readlines()

def calc_area(dims: str) -> int:
    dims = sorted(map(int, dims.split('x')))
    dims.append(dims[0])
    return sum(2*a * b for a, b in pairwise(dims)) + dims[0]*dims[1]

def calc_ribbon(dims: str) -> int:
    dims = sorted(map(int, dims.split('x')))
    dims.append(dims[0])
    return dims[0]*dims[1]*dims[2] + 2*dims[0] + 2*dims[1]

print(sum(calc_area(dims) for dims in lines))
print(sum(calc_ribbon(dims) for dims in lines))
