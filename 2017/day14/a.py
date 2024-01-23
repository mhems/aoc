from sys import argv
from operator import xor
from functools import reduce

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

def rounds(s: str) -> str:
    data = list(range(256))
    lengths = [ord(l) for l in s] + [17, 31, 73, 47, 23]
    pos, skip = 0, 0
    for _ in range(64):
        data, pos, skip = knot_hash(data, lengths, pos, skip) 
    dense = [reduce(xor, data[i:i+16]) for i in range(0, 256, 16)]
    return ''.join((hex(e)[2:]).rjust(2, '0') for e in dense)

def get_row(key: str, i: int) -> [bool]:
    hash = rounds(key + "-" + str(i))
    binary = bin(int(hash, 16))[2:].rjust(128, '0')
    return [bit == '1' for bit in binary]

def make_grid(key: str) -> [[bool]]:
    return [get_row(key, i) for i in range(128)]

key = argv[1]
grid = make_grid(key)
print(sum(sum(int(b) for b in row) for row in grid))
