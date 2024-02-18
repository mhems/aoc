program = [int(token) for token in open('input.txt').read().strip().split(',')]

def execute(program: [int], noun=12, verb=2) -> int:
    ip = 0
    program[1] = noun
    program[2] = verb
    while ip < len(program) and program[ip] != 99:
        op, a, b, c = program[ip: ip+4]
        program[c] = program[a] + program[b] if op == 1 else program[a] * program[b]
        ip += 4
    return program[0]

def find(program: [int], target: int) -> int:
    for noun in range(0, 100):
        for verb in range(0, 100):
            if target == execute(list(program), noun, verb):
                return 100 * noun + verb

print(execute(list(program)))
print(find(list(program), 19690720))
