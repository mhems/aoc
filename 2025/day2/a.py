import sys
from itertools import batched

def is_repetition(id: int) -> int:
    s = str(id)
    half = len(s)//2
    if len(set(s)) <= half:
        for chunk_size in range(half, 0, -1):
            if len(s) % chunk_size == 0:
                chunks = list(batched(s, chunk_size))
                if all(chunk == chunks[0] for chunk in chunks[1:]):
                    return len(chunks)
    return 0

slices = [tuple(map(int, slice.split('-'))) for slice in open(sys.argv[1]).read().split(',')]
part1, part2 = 0, 0
for start, stop in slices:
    for id in range(start, stop+1):
        n = is_repetition(id)
        if n > 0:
            part2 += id
            if n == 2:
                part1 += id

print(part1)
print(part2)
