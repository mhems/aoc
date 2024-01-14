from sys import argv
from collections import namedtuple as nt
from time import sleep

Cmd = nt('Cmd', ['op', 'a', 'b'])

with open(argv[1]) as fp:
    lines = fp.readlines()

def parse_cmd(s: str) -> Cmd:
    tokens = s.split()
    if tokens[0] in ('cpy', 'jnz'):
        try:
            a = int(tokens[1])
        except ValueError:
            a = tokens[1]
        b = int(tokens[2]) if tokens[0] == 'jnz' else tokens[2]
        return Cmd(tokens[0], a, b)
    else:
        return Cmd(tokens[0], tokens[1], 0)

cmds = [parse_cmd(line.strip()) for line in lines]
regs = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
pc = 0

def run_cmd(cmd: Cmd):
    global pc
    val = regs[cmd.a] if isinstance(cmd.a, str) else cmd.a
    if cmd.op == 'jnz':
        if val != 0:
            pc += cmd.b
        else:
            pc += 1
    else:
        if cmd.op == 'inc':
            regs[cmd.a] += 1
        elif cmd.op == 'dec':
            regs[cmd.a] -= 1
        elif cmd.op == 'out':
            print(regs[cmd.a], flush=True, end='')
            sleep(0.1)
        else:
            regs[cmd.b] = val
        pc += 1

def run(cmds, a: int):
    regs['a'] = a
    while True:
        if pc >= len(cmds):
            break
        run_cmd(cmds[pc])

n = 0xAAA - 365 * 7
run(cmds, n)
