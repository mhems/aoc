from sys import argv

def simulate(regs: [int], prog: [int]) -> str:
    def combo(value: int) -> int:
        if value < 4:
            return value
        return regs[value - 4]
    pc = 0
    output = []
    while pc < len(prog):
        opcode, operand = prog[pc], prog[pc + 1]
        if opcode == 0:
            regs[0] = regs[0] // (2 ** combo(operand))
            pc += 2
        elif opcode == 1:
            regs[1] = regs[1] ^ operand
            pc += 2
        elif opcode == 2:
            regs[1] = combo(operand) % 8
            pc += 2
        elif opcode == 3:
            if regs[0] == 0:
                pc += 2
            else:
                pc = operand
        elif opcode == 4:
            regs[1] = regs[1] ^ regs[2]
            pc += 2
        elif opcode == 5:
            output.append(combo(operand) % 8)
            pc += 2
        elif opcode == 6:
            regs[1] = regs[0] // (2 ** combo(operand))
            pc += 2
        elif opcode == 7:
            regs[2] = regs[0] // (2 ** combo(operand))
            pc += 2
    return ','.join(map(str, output))

regs, prog = open(argv[1]).read().split('\n\n')
regs = [int(line.strip().split()[-1]) for line in regs.strip().split('\n')]
prog = [int(e) for e in prog.strip().split()[-1].split(',')]
print(simulate(regs, prog))
print(simulate([int(argv[2]), 0, 0], prog))
