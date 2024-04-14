range_pairs = [tuple(map(lambda s: tuple(map(int, s.split('-'))), line.strip().split(',')))
               for line in open('input.txt').readlines()]

def subrange(a: (int, int), b: (int, int)) -> bool:
    return b[0] >= a[0] and b[1] <= a[1]

def overlap(a: (int, int), b: (int, int)) -> bool:
    return b[0] <= a[0] <= b[1] or b[0] <= a[1] <= b[1]

print(sum(int(subrange(a, b) or subrange(b, a)) for a, b in range_pairs))
print(sum(int(overlap(a, b) or overlap(b, a)) for a, b in range_pairs))
