def get_n_by_pos(i: int, j: int) -> int:
    r = 1
    delta = 1
    for _ in range(1, i):
        r += delta
        delta += 1
    delta = i + 1
    for _ in range(1, j):
        r += delta
        delta += 1
    return r

def naive_gen(n: int) -> int:
    v = n * 252533
    return v % 33554393

def get_nth_in_seq(n: int) -> int:
    v = 20151125
    for _ in range(n-1):
        v = naive_gen(v)
    return v

with open('input.txt') as fp:
    lines = fp.readlines()
i, j = [int(line.strip()) for line in lines]
n = get_n_by_pos(i, j)
v = get_nth_in_seq(n)
print(v)
