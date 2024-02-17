from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

def make_map(lines: str) -> {str: str}:
    map = {}
    for line in lines:
        tokens = line.strip().split('=>')
        map[tokens[0].strip()] = tokens[1].strip()
    return map

def score(state: str, start: int):
    return sum((i-start) for i, c in enumerate(state) if c == '#')

def generate(state: str, map: {str: str}, n: int) -> int:
    start = 0
    prev_score = None
    prev_diff = None
    diff = None
    for i in range(n):
        state = '.....' + state + '.....'
        new_state = ''
        for pos in range(len(state) - 5):
            new_state += map[state[pos:pos+5]]
        state = new_state
        start += 3
        total = score(state, start)
        if prev_score is not None:
            diff = total - prev_score
        if diff is not None and prev_diff is not None and diff == prev_diff:
            return total + diff * (n - i - 1)
        prev_score = total
        prev_diff = diff
    return score(state, start)

state = lines[0].split(':')[1].strip()
map = make_map(lines[2:])
print(generate(state, map, 20))
print(generate(state, map, 50000000000))
