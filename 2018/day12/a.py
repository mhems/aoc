from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

def make_map(lines: str) -> {str: str}:
    map = {}
    for line in lines:
        tokens = line.strip().split('=>')
        map[tokens[0].strip()] = tokens[1].strip()
    return map

def generate(state: str, map: {str: str}, n: int) -> int:
    start = 0
    for _ in range(n):
        state = '.....' + state + '.....'
        new_state = ''
        for pos in range(len(state) - 5):
            new_state += map[state[pos:pos+5]]
        state = new_state
        start += 3
        #print(state)
    return sum((i-start) for i, c in enumerate(state) if c == '#')

state = lines[0].split(':')[1].strip()
map = make_map(lines[2:])
print(generate(state, map, 20))
