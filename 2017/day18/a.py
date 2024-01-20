from sys import argv
from collections import namedtuple as nt
from operator import mul, mod

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
sounds = []

def lookup(arg):
    if isinstance(arg, int):
        return arg
    if arg not in regs:
        regs[arg] = 0
    return regs[arg]

def run_op(op: Op, early_stop: bool = True):
    global regs, pc, sounds
    if op.name == 'jgz':
        if lookup(op.args[0]) > 0:
            pc += lookup(op.args[1])
        else:
            pc += 1
    else:
        if op.name == 'set':
            regs[op.args[0]] = lookup(op.args[1])
        elif op.name == 'add':
            regs[op.args[0]] = sum(map(lookup, op.args))
        elif op.name == 'mul':
            regs[op.args[0]] = mul(*map(lookup, op.args))
        elif op.name == 'mod':
            regs[op.args[0]] = mod(*map(lookup, op.args))
        elif op.name == 'snd':
            sounds.append(lookup(op.args[0]))
        elif op.name == 'rcv':
            if lookup(op.args[0]) != 0:
                sound = sounds.pop()
                if early_stop:
                    raise ValueError(sound)
        pc += 1

def run(ops: [Op], early_stop: bool = True):
    global pc
    try:
        while pc < len(ops):
            run_op(ops[pc], early_stop)
    except ValueError as e:
        print(e)

ops = [parse_op(line.strip()) for line in lines]
run(ops)
