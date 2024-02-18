from sys import argv

program = [int(token) for token in open(argv[1]).read().strip().split(',')]

def decode(n: int) -> (int, int, int):
    op = n % 100
    mode1 = n % 1000 // 100
    mode2 = n % 10000 // 1000
    return op, mode1, mode2

def arg(a: int, mode: int, program: [int]) -> int:
    if mode == 0:
        return program[a]
    return a

def execute(program: [int], input: [int], output: [int]) -> int:
    ip = 0
    while ip < len(program) and program[ip] != 99:
        op, mode1, mode2 = decode(program[ip])
        a = arg(program[ip+1], mode1, program)
        if op not in (3, 4):
            b = arg(program[ip+2], mode2, program)
        if op in (1, 2, 7, 8):
            if op == 1:
                result = a + b
            elif op == 2:
                result = a * b
            elif op == 7:
                result = int(a < b)
            elif op == 8:
                result = int(a == b)
            program[program[ip+3]] = result
            ip += 4
        elif op in (3, 4):
            if op == 3:
                program[program[ip+1]] = input.pop(0)
            else:
                output.append(a)
            ip += 2
        elif op in (5, 6):
            if op == 5:
                if a != 0:
                    ip = b
                else:
                    ip += 3
            else:
                if a == 0:
                    ip = b
                else:
                    ip += 3
        else:
            raise ValueError(op, program[ip])
    return program[0]

output = []
execute(list(program), [1], output)
print(output[-1])

output.clear()
execute(list(program), [5], output)
print(output[-1])
