from sys import argv
from itertools import cycle

def make_pattern(i: int) -> [int]:
    return [0] * i + [1] * i + [0] * i + [-1] * i

def fft(number: [int]) -> [int]:
    answer = [None] * len(number)
    number.insert(0, 0)
    for i in range(1, len(number)):
        pattern = make_pattern(i)
        n = sum(a * b for a, b in zip(cycle(pattern), number))
        answer[i-1] = abs(n) % 10
    return answer

def phased_fft(number: [int], n: int = 100) -> str:
    for _ in range(n):
        number = fft(number)
    return ''.join(map(str, number))[:8]

numbers = [[int(digit) for digit in str(int(line.strip()))] for line in open(argv[1]).readlines()]

for number in numbers:
    print(phased_fft(number))
