from sys import argv
import numpy as np
from math import ceil

def make_pattern(i: int, n: int) -> [int]:
    pattern = [0] * i
    count = i
    if count < n + 1:
        pattern += [1] * i
        count += i
    if count < n + 1:
        pattern += [0] * i
        count += i
    if count < n + 1:
        pattern += [-1] * i
        count += i
    if count < n + 1:
        rep = ceil(n/len(pattern)) + 1
        pattern *= rep
    pattern.pop(0)
    if len(pattern) > n:
        pattern = pattern[:n]
    return pattern

def make_patterns(n: int):
    return np.array([make_pattern(i + 1, n) for i in range(n)])

matmod = np.vectorize(lambda n: abs(n) % 10)

def fft(number: [int], pattern) -> [int]:
    product = np.matmul(pattern, number)
    return matmod(product)

def phased_fft(number, phases: int = 100) -> str:
    pattern = make_patterns(len(number))
    number = [int(digit) for digit in number]
    number = np.array(number).reshape((len(number), 1))
    for _ in range(phases):
        number = fft(number, pattern)
    return ''.join(map(str, number.flat))

def part2(number: str, repeat=10_000) -> str:
    index = int(number[:7])
    result = phased_fft(number * repeat)
    return ''.join(str(result[i][0]) for i in range(index, index+8))

numbers = [line.strip() for line in open(argv[1]).readlines()]
for number in numbers:
    print(phased_fft(number)[:8])
    #print(part2(number, 10))
    print()
