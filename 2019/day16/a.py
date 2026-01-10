import sys
import numpy as np
from tqdm import tqdm

mod = lambda n: abs(n) % 10

def phase(digits: np.array):
    n = len(digits)
    result = np.zeros(n, dtype=np.int32)
    mid = n//2
    result[0] = digits[0]
    running = digits[0]
    for i in range(1, mid):
        running -= digits[i-1]
        running += digits[i+i-1] + digits[i+i]
        result[i] = running
    running -= digits[mid-1]
    running += digits[-1]
    result[mid] = running % 10
    offset = mid
    for i in range(mid + 1, n):
        running -= digits[offset]
        offset += 1
        result[i] = running % 10
    start = 2
    row = 0
    while start < n:
        factor = -1
        i = start
        stride = row + 1
        while i < n:
            result[row] += factor * sum(digits[i:i+stride])
            i += 2 * stride
            factor *= -1
        result[row] = mod(result[row])
        start += 3
        row += 1
    assert row < mid
    for i in range(row, mid):
        result[i] = mod(result[i])
    return result

def phases(seed):
    signal = seed
    for _ in range(100):
        signal = phase(signal)
    return signal[:8]

def phase_part2(digits: np.array):
    n = len(digits)
    result = np.zeros(n, dtype=np.int32)
    running = sum(digits)
    result[0] = running % 10
    for i in range(1, n):
        running -= digits[i-1]
        result[i] = running % 10
    return result

def phases2(seed, repeat=10_000) -> str:
    index = int(''.join(map(str, seed[:7])))
    s = len(seed)
    start = index//s * s
    amt = s * repeat - start
    signal = np.tile(seed, amt//s)[:amt]
    for _ in tqdm(range(100)):
        signal = phase_part2(signal)
    offset = index - start
    return signal[offset:offset+8]

numbers = [np.array(list(map(int, line.strip())), dtype=np.int32)
           for line in open(sys.argv[1]).readlines()]
for num in numbers:
    print(''.join(map(str, phases(num))))
    print(''.join(map(str, phases2(num))))
