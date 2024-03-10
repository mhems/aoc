from sys import argv

def parse(line: str) -> (str, int):
    tokens = line.split()
    return tokens[0], int(tokens[1])

def detect_loop(instructions: [(str, int)], err: bool = False) -> int:
    seen = set()
    acc = 0
    pc = 0
    while pc < len(instructions):
        if pc in seen:
            return acc if not err else None
        seen.add(pc)
        op, arg = instructions[pc]
        if op == 'jmp':
            pc += arg
        else:
            if op == 'acc':
                acc += arg
            pc += 1
    return acc

def generate_candidates(instructions: [(str, int)]):
    for i, (op, arg) in enumerate(instructions):
        if op != 'acc':
            yield list(instructions[:i]) + [('nop' if op == 'jmp' else 'jmp', arg)] + list(instructions[i+1:])

def fix_program(instructions: [(str, int)]) -> int:
    for candidate in generate_candidates(instructions):
        if (a := detect_loop(candidate, True)) is not None:
            return a

instructions = [parse(line.strip()) for line in open(argv[1]).readlines()]
print(detect_loop(instructions))
print(fix_program(instructions))
