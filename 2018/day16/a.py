from sys import argv

def num_matches(initial: [int], _: int, a: int, b: int, c: int, final: [int]) -> int:
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
    count = 0
    for op in ops.values():
        regs.extend(initial)
        regs[c] = op(a, b)
        if regs == final:
            count += 1
        regs.clear()
    return count

def parse_case(text: str) -> ([int], [int], [int]):
    lines = text.strip().split('\n')
    initial = [int(n) for n in lines[0][9:-1].split(', ')]
    cmd = [int(n) for n in lines[1].split()]
    final = [int(n) for n in lines[2][9:-1].split(', ')]
    return initial, cmd, final

with open(argv[1]) as fp:
    text = fp.read()

cases, program = text.split('\n' * 4)
cases = [parse_case(chunk) for chunk in cases.split('\n' * 2)]
print(sum(int(num_matches(initial, *instruction, final) >= 3) for initial, instruction, final in cases))
