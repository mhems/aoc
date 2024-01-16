from sys import argv
from collections import namedtuple as nt

Cmd = nt('Cmd', ['name', 'arg1', 'arg2'])

with open(argv[1]) as fp:
    lines = fp.readlines()
lines.pop(0)
initial = argv[2]

def parse_cmd(line: str) -> Cmd:
    tokens = line.strip().split()
    if tokens[0] == 'swap':
        if tokens[1] == 'position':
            return Cmd('swap_pos', int(tokens[2]), int(tokens[-1]))
        return Cmd('swap_ch', tokens[2], tokens[-1])
    if tokens[0] == 'rotate':
        if tokens[1] == 'based':
            return Cmd('rotate', tokens[-1], None)
        if tokens[1] == 'left':
            return Cmd('lshift', int(tokens[2]), None)
        return Cmd('rshift', int(tokens[2]), None)
    if tokens[0] == 'move':
        return Cmd('move', int(tokens[2]), int(tokens[-1]))
    return Cmd('reverse', int(tokens[2]), int(tokens[-1]))

def swap_pos(s: str, pos1: int, pos2: int) -> str:
    list_ = list(s)
    list_[pos1], list_[pos2] = list_[pos2], list_[pos1]
    return ''.join(list_)

def swap_letter(s: str, ch1: str, ch2: str) -> str:
    return swap_pos(s, s.index(ch1), s.index(ch2))

def rotate(s: str, ch: str) -> str:
    index = s.index(ch)
    shift = {1: 1, 3: 2, 5: 3, 7: 4, 2: 6, 4: 7, 6: 0, 0: 1}[index]
    return rshift(s, shift)

def lshift(s: str, amt: int) -> str:
    return s[-amt:] + s[:-amt]

def rshift(s: str, amt: int) -> str:
    return s[amt:] + s[:amt]

def move(s: str, src_pos: int, dst_pos: int) -> str:
    src = s[dst_pos]
    list_ = list(s[:dst_pos] + s[dst_pos+1:])
    list_.insert(src_pos, src)
    return ''.join(list_)
    
def reverse(s: str, start_pos: int, stop_pos: int) -> str:
    sub = s[start_pos: stop_pos + 1]
    return s[:start_pos] + str(''.join(reversed(sub))) + s[stop_pos + 1:]

def run_cmd(s: str, cmd: Cmd) -> str:
    if cmd.name == 'swap_pos':
        return swap_pos(s, cmd.arg1, cmd.arg2)
    if cmd.name == 'swap_ch':
        return swap_letter(s, cmd.arg1, cmd.arg2)
    if cmd.name == 'rotate':
        return rotate(s, cmd.arg1)
    if cmd.name == 'lshift':
        return lshift(s, cmd.arg1)
    if cmd.name == 'rshift':
        return rshift(s, cmd.arg1)
    if cmd.name == 'move':
        return move(s, cmd.arg1, cmd.arg2)
    return reverse(s, cmd.arg1, cmd.arg2)

def mutate(s: str, cmds: [Cmd]) -> str:
    for cmd in cmds:
        s = run_cmd(s, cmd)
    return s

cmds = list(reversed([parse_cmd(line.strip()) for line in lines]))
print(mutate(initial, cmds))
