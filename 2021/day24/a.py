from itertools import product
from tqdm import tqdm

def parse(line: str) -> (str, str, str):
    tokens = line.strip().split()
    if len(tokens) > 2 and tokens[-1][-1].isdigit():
        return tokens[0], tokens[1], int(tokens[2])
    return tuple(tokens)

def execute(instructions: tuple, num: str) -> bool:
    regs = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    def access(arg) -> int:
        return arg if isinstance(arg, int) else regs[arg]
    input_index = 0
    assert '0' not in num
    for op, a, *b in instructions:
        if op == 'inp':
            if input_index >= len(num):
                break
            regs[a] = int(num[input_index])
            input_index += 1
            continue
        b = b[0]
        if op == 'add':
            regs[a] += access(b)
        elif op == 'mul':
            regs[a] *= access(b)
        elif op == 'div':
            regs[a] //= access(b)
        elif op == 'mod':
            regs[a] %= access(b)
        else:
            if b == 'w':
                if input_index in (4, 8, 9, 11, 12, 13, 14) and regs[a] != regs[b]:
                    return False
            regs[a] = int(regs[a] == access(b))
    return input_index < 14 or regs['z'] == 0

def bfs(instructions: tuple) -> {int}:
    q = set()
    for n in product(range(1, 10), repeat=4):
        num = ''.join(map(str, n))
        if execute(instructions, num):
            q.add(num)
    print(len(q))
    
    r = set()
    for e in tqdm(q):
        for n in product(range(1, 10), repeat=4):
            num = e + ''.join(map(str, n))
            if execute(instructions, num):
                r.add(num)
    print(len(r))
    
    s = set()
    for e in tqdm(r):
        for n in range(1, 10):
            num = e + str(n)
            if execute(instructions, num):
                s.add(num)
    print(len(s))
    
    t = set()
    for e in tqdm(s):
        for n in product(range(1, 10), repeat=2):
            num = e + ''.join(map(str, n))
            if execute(instructions, num):
                t.add(num)
    print(len(t))
    
    u = set()
    for e in tqdm(t):
        for n in range(1, 10):
            num = e + str(n)
            if execute(instructions, num):
                u.add(num)
    print(len(u))
    
    v = set()
    for e in tqdm(u):
        for n in range(1, 10):
            num = e + str(n)
            if execute(instructions, num):
                v.add(num)
    print(len(v))
    
    w = set()
    for e in tqdm(v):
        for n in range(1, 10):
            num = e + str(n)
            if execute(instructions, num):
                w.add(num)
    print(len(w))
    
    return set(map(int, w))

instructions = [parse(line.strip()) for line in open('input.txt').readlines()]
accepted = bfs(instructions)
print(max(accepted))
print(min(accepted))
