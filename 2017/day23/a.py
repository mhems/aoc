from sys import argv
from collections import namedtuple as nt
from operator import sub, mul, mod

Op = nt('Op', ['name', 'args'])

with open(argv[1]) as fp:
    lines = fp.readlines()

def parse_arg(arg):
    try:
        return int(arg)
    except ValueError:
        return arg

def parse_op(line: str) -> Op:
    tokens = line.strip().split()
    return Op(tokens[0], [parse_arg(arg) for arg in tokens[1:]])

regs = {}
pc = 0

def lookup(arg):
    if isinstance(arg, int):
        return arg
    if arg not in regs:
        regs[arg] = 0
    return regs[arg]

def run_op(op: Op) -> int:
    global regs, pc
    if op.name == 'jnz':
        #print(pc, regs)
        if lookup(op.args[0]) != 0:
            pc += lookup(op.args[1])
        else:
            pc += 1
    else:
        if op.name == 'set':
            regs[op.args[0]] = lookup(op.args[1])
        elif op.name == 'sub':
            regs[op.args[0]] = sub(*map(lookup, op.args))
        elif op.name == 'mul':
            regs[op.args[0]] = mul(*map(lookup, op.args))
        elif op.name == 'mod':
            if lookup(op.args[1]) % lookup(op.args[2]) == 0:
                regs[op.args[0]] = 0
        pc += 1
    return int(op.name == 'mul')

def run(ops: [Op]):
    global pc
    num_muls = 0
    while pc < len(ops):
        num_muls += run_op(ops[pc])
    return num_muls

ops = [parse_op(line.strip()) for line in lines]
print(run(ops))

h = 0
for i in range(int(argv[2]), int(argv[3]) + 1, int(argv[4])):
    for c in range(2, i):
        if i % c == 0:
            h += 1
            break
print(h)

regs = {'a': 1}
pc = 0
run(ops)
print(regs['h'])
