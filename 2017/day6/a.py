from sys import argv

with open(argv[1]) as fp:
    banks = list(map(int, fp.read().split()))

def reallocate(banks: [int]):
    biggest = banks[0]
    biggest_index = 0
    for i in range(1, len(banks)):
        if banks[i] > biggest:
            biggest = banks[i]
            biggest_index = i
    banks[biggest_index] = 0
    for i in range(biggest):
        banks[(biggest_index + 1 + i) % len(banks)] += 1

def cycle(banks: [int]) -> int:
    i = 0
    seen = set()
    seen.add((i, tuple(banks)))
    while True:
        reallocate(banks)
        i += 1
        t = tuple(banks)
        for index, element in seen:
            if t == element:
                return i, i - index
        seen.add((i, t))

print(cycle(banks))
