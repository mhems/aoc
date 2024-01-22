from sys import argv
from collections import namedtuple as nt
from operator import lt, le, eq, ne, gt, ge

Condition = nt('Condition', ['reg', 'op', 'val'])
Op = nt('Op', ['reg', 'inc', 'val', 'condition'])

with open(argv[1]) as fp:
    lines = fp.readlines()

def parse_condition(text: str) -> Condition:
    ops = {'>': gt, '>=': ge, '<': lt, '<=': le, '==': eq, '!=': ne}
    tokens = text.strip().split()
    return Condition(tokens[0], ops[tokens[1]], int(tokens[2]))

def parse_op(text: str) -> Op:
    tokens = text.strip().split()
    return Op(tokens[0], tokens[1] == 'inc', int(tokens[2]), parse_condition(' '.join(tokens[4:])))

regs = {}

def lookup(reg: str) -> int:
    if reg not in regs:
        regs[reg] = 0
    return regs[reg]

def run(ops: [Op]):
    biggest = 0
    for op in ops:
        if op.condition.op(lookup(op.condition.reg), op.condition.val):
            regs[op.reg] = lookup(op.reg) + (op.val if op.inc else -op.val)
            biggest = max(biggest, max(regs.values()))
    return biggest

ops = [parse_op(line.strip()) for line in lines]
biggest = run(ops)
print(max(regs.values()))
print(biggest)
