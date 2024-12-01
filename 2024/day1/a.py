from sys import argv

left = []
right = []

with open(argv[1]) as fp:
    for line in fp.readlines():
        l, r = map(int, line.strip().split())
        left.append(l)
        right.append(r)

print(sum(abs(l - r) for l, r in zip(sorted(left), sorted(right))))
print(sum(l * right.count(l) for l in left))
