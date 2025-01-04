from sys import argv

def to_run(seq: str) -> ((int)):
    runs = []
    i = 0
    L = len(seq)
    while i < L:
        if seq[i] == '?':
            runs.append(('?', 1))
            i += 1
        else:
            start = i
            while i < L and seq[i] == seq[start]:
                i += 1
            runs.append((seq[start], i - start))
    return tuple(runs)

def parse(line: str) -> (((int)), (int)):
    seq, nums = line.split()
    return to_run(seq), tuple(map(int, nums.split(',')))

def cache(func):
    store = dict()
    def inner(run: ((int)), sizes: (int), acc: int = 0, must_clear: bool = False, *args, **kwargs):
        key = (run, sizes, acc, must_clear)
        value = store.get(key)
        if value is not None:
            return value
        store[key] = func(run, sizes, acc, must_clear, *args, **kwargs)
        return store[key]
    return inner

@cache
def num_ways(run: ((int)), sizes: (int), acc: int = 0, must_clear: bool = False) -> int:
    if not run:
        return int(not sizes)
    if not sizes:
        return int(not any(val == '#' for val, _ in run))
    cur_val, cur_size = run[0]
    if cur_val == '?':
        total = 0
        if not must_clear:
            a = acc + 1
            if a == sizes[0]:
                total += num_ways(run[1:], sizes[1:], 0, True)
            elif a < sizes[0]:
                total += num_ways(run[1:], sizes, a, False)
        if acc == 0:
            total += num_ways(run[1:], sizes, 0, False)
        return total
    elif cur_val == '.':
        if acc != 0:
            return 0
        return num_ways(run[1:], sizes, 0, False)
    else:
        if must_clear:
            return 0
        a = acc + cur_size
        if a == sizes[0]:
            return num_ways(run[1:], sizes[1:], 0, True)
        elif a < sizes[0]:
            return num_ways(run[1:], sizes, a, False)
    return 0

lines = [line.strip() for line in open(argv[1]).readlines()]
pairs = [parse(line) for line in lines]
print(sum(num_ways(run, sizes) for run, sizes in pairs))

unfolded_pairs = [(to_run('?'.join([line.split()[0]] * 5)), sizes * 5) for line, (_, sizes) in zip(lines, pairs)]
print(sum(num_ways(run, sizes) for run, sizes in unfolded_pairs))
