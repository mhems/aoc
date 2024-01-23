from sys import argv
from operator import xor
from functools import reduce

with open(argv[1]) as fp:
    text = fp.read()
n = int(argv[2])

def knot_hash(data: [int], lengths: [int], pos: int = 0, skip: int = 0) -> ([int], int, int):
    for length in lengths:
        end_pos = pos + length
        if end_pos > len(data):
            end = data[pos:]
            start = data[:(end_pos % len(data))]
            rev = list(reversed(end + start))
            for i, r in zip(range(pos, end_pos), rev):
                data[i % len(data)] = r
        else:
            data = data[:pos] + list(reversed(data[pos:end_pos])) + data[end_pos:]
        pos = (pos + length + skip) % len(data)
        skip += 1
    return (data, pos, skip)

lengths = [int(token) for token in text.split(',')]
nums = list(range(n))
data, _, _ = knot_hash(nums, lengths)
print(data[0] * data[1])

def rounds(data: [int], s: str) -> str:
    lengths = [ord(l) for l in s] + [17, 31, 73, 47, 23]
    pos, skip = 0, 0
    for _ in range(64):
        data, pos, skip = knot_hash(data, lengths, pos, skip) 
    dense = [reduce(xor, data[i:i+16]) for i in range(0, 256, 16)]
    return ''.join((hex(e)[2:]).rjust(2, '0') for e in dense)

print(rounds(nums, text.strip()))
