with open('input.txt') as fp:
    lines = fp.readlines()

ranges = sorted(tuple(map(int, line.strip().split('-'))) for line in lines)

def merge(ranges: [(int, int)]) -> [(int, int)]:
    i = 0
    cons = []
    while i < len(ranges):
        start, end = ranges[i]
        next_start, next_end = ranges[i+1]
        while start <= next_start <= end or next_start == end + 1:
            end = max(end, next_end)
            i += 1
            if i >= len(ranges) - 1:
                cons.append((start, end))
                return cons
            next_start, next_end = ranges[i+1]
        cons.append((start, end))
        i += 1
    return cons

merged = merge(ranges)

print(merged[0][1] + 1)

d = 0
for i in range(1, len(merged)):
    d += merged[i][0] - merged[i-1][1] - 1
d += 4294967295 - merged[-1][1]

print(d)
