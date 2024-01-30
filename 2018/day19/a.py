from sys import argv

regs = [0] * 6
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

def parse_command(line: str) -> (str, int, int, int):
    tokens = line.strip().split()
    return tuple([tokens[0]] + list(map(int, tokens[1:])))

def execute(program: [(str, int, int, int)], ip_index: int) -> [int]:
    global regs, ops
    while regs[ip_index] < len(program):
        opcode, a, b, c = program[regs[ip_index]]
        regs[c] = ops[opcode](a, b)
        regs[ip_index] += 1
    return regs

with open(argv[1]) as fp:
    lines = fp.readlines()

ip = int(lines.pop(0).split()[1])
program = [parse_command(line.strip()) for line in lines]
print(execute(program, ip))

regs = [0] * 6
regs[0] = 1
print(execute(program, ip))