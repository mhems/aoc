from sys import argv
from collections import namedtuple as nt

Cmd = nt('Cmd', ['op', 'a', 'b'])

with open(argv[1]) as fp:
    lines = fp.readlines()

def parse_cmd(s: str) -> Cmd:
    tokens = s.split()
    if tokens[0] in ('cpy', 'jnz', 'tgl'):
        try:
            a = int(tokens[1])
        except ValueError:
            a = tokens[1]
        b = None
        if tokens[0] != 'tgl':
            try:
                b = int(tokens[2])
            except ValueError:
                b = tokens[2]
        return Cmd(tokens[0], a, b)        
    else:
        return Cmd(tokens[0], tokens[1], None)

cmds = [parse_cmd(line.strip()) for line in lines]
regs = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
pc = 0

def toggle(amt: int):
    global pc
    index = pc + amt
    if index < len(cmds):
        cmd = cmds[pc + amt]
        if cmd.op in ('inc', 'dec', 'tgl'):
            new_cmd = Cmd('dec' if cmd.op == 'inc' else 'inc', cmd.a, None)
        elif cmd.op == 'jnz':
            if isinstance(cmd.b, int):
                new_cmd = Cmd('inv', None, None)
                print('made instruction', index, 'invalid:', cmd)
            else:
                new_cmd = Cmd('cpy', cmd.a, cmd.b)
        elif cmd.op == 'cpy':
            new_cmd = Cmd('jnz', cmd.a, cmd.b)
        else:
            raise ValueError(cmd.op)
        cmds[index] = new_cmd
    pc += 1

def run_cmd(cmd: Cmd):
    global pc
    val = regs[cmd.a] if isinstance(cmd.a, str) else cmd.a
    if cmd.op == 'jnz':
        if val != 0:
            pc += cmd.b if isinstance(cmd.b, int) else regs[cmd.b]
        else:
            pc += 1
    elif cmd.op == 'tgl':
        toggle(val)
    else:
        if cmd.op == 'inc':
            regs[cmd.a] += 1
        elif cmd.op == 'dec':
            regs[cmd.a] -= 1
        else:
            regs[cmd.b] = val
        pc += 1

def run(cmds):
    while True:
        if pc >= len(cmds):
            break
        run_cmd(cmds[pc])
    return regs['a']

regs['a'] = 7
print(run(cmds))

pc = 0
cmds = [parse_cmd(line.strip()) for line in lines]
regs = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
regs['a'] = 12
print(run(cmds))
