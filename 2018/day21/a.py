from sys import argv

regs = [0] * 6
ops = {
    'addi': lambda a, b: regs[a] + b,
    'addr': lambda a, b: regs[a] + regs[b],
    'muli': lambda a, b: regs[a] * b,
    'mulr': lambda a, b: regs[a] * regs[b],
    'divi': lambda a, b: regs[a] // b,
    'bani': lambda a, b: regs[a] & b,
    'banr': lambda a, b: regs[a] & regs[b],
    'bori': lambda a, b: regs[a] | b,
    'borr': lambda a, b: regs[a] | regs[b],
    'modr': lambda a, b: int(regs[a] % regs[b] == 0),
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

def execute(program: [(str, int, int, int)], ip_index: int):
    global regs, ops
    num_done = 0
    s = set()
    big = set()
    while regs[ip_index] < len(program):
        opcode, a, b, c = program[regs[ip_index]]
        regs[c] = ops[opcode](a, b)
        regs[ip_index] += 1
        num_done += 1
        if regs[ip_index] == 28:
            if len(s) == 0:
                print(regs[4])
            if regs[4] in s:
                print(max(big, key=lambda p: p[0])[1])
                return
            s.add(regs[4])
            big.add((num_done, regs[4]))

with open(argv[1]) as fp:
    lines = fp.readlines()

ip = int(lines.pop(0).split()[1])
program = [parse_command(line.strip()) for line in lines]
regs = [0] * 6
execute(program, ip)
