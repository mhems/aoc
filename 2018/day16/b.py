from sys import argv

regs = []
ops = {
    'addi': lambda a, b: regs[a] + b,
    'addr': lambda a, b: regs[a] + regs[b],
    'muli': lambda a, b: regs[a] * b,
    'mulr': lambda a, b: regs[a] * regs[b],
    'bani': lambda a, b: regs[a] & b,
    'banr': lambda a, b: regs[a] & regs[b],
    'bori': lambda a, b: regs[a] | b,
    'borr': lambda a, b: regs[a] | regs[b],
    'seti': lambda a, _: a,
    'setr': lambda a, _: regs[a],
    'gtir': lambda a, b: int(a > regs[b]),
    'gtri': lambda a, b: int(regs[a] > b),
    'gtrr': lambda a, b: int(regs[a] > regs[b]),
    'eqir': lambda a, b: int(a == regs[b]),
    'eqri': lambda a, b: int(regs[a] == b),
    'eqrr': lambda a, b: int(regs[a] == regs[b]),
}

def matches(initial: [int], _: int, a: int, b: int, c: int, final: [int]):
    global regs, ops
    candidates = set()
    for name, op in ops.items():
        regs.extend(initial)
        regs[c] = op(a, b)
        if regs == final:
            candidates.add(name)
        regs.clear()
    return candidates

def parse_case(text: str) -> ([int], [int], [int]):
    lines = text.strip().split('\n')
    initial = [int(n) for n in lines[0][9:-1].split(', ')]
    cmd = [int(n) for n in lines[1].split()]
    final = [int(n) for n in lines[2][9:-1].split(', ')]
    return initial, cmd, final

def deduce(cases: [([int], [int], [int])]) -> {int: str}:
    map = {i : None for i in range(16)}
    for initial, instruction, final in cases:
        opcode = instruction[0]
        cands = matches(initial, *instruction, final)
        if map[opcode] is None:
            map[opcode] = cands
        else:
            map[opcode] = map[opcode].intersection(cands)
    while any(len(cands) > 1 for cands in map.values()):
        for opcode, cands in map.items():
            if len(cands) == 1:
                for o, ops in map.items():
                    if opcode != o:
                        map[o] = ops - cands
    return {opcode: next(iter(cands)) for opcode, cands in map.items()}

def execute(mapping: {int: str}, program: [[int]]) -> [int]:
    global regs, ops
    regs.clear()
    regs.extend([0, 0, 0, 0])
    for opcode, a, b, c in program:
        regs[c] = ops[mapping[opcode]](a, b)
    return regs

with open(argv[1]) as fp:
    text = fp.read()

cases, program = text.split('\n' * 4)
cases = [parse_case(chunk) for chunk in cases.split('\n' * 2)]
mapping = deduce(cases)
program = [list(map(int, line.strip().split())) for line in program.strip().split('\n')]
print(execute(mapping, program))
