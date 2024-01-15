from sys import argv
from collections import namedtuple as nt

Cmd = nt('Cmd', ['name', 'arg1', 'arg2'])

with open(argv[1]) as fp:
    lines = fp.readlines()
initial = lines.pop(0).strip()

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
    if index >= 4:
        index += 1
    index += 1
    return rshift(s, index % len(s))

def lshift(s: str, amt: int) -> str:
    return s[amt:] + s[:amt]

def rshift(s: str, amt: int) -> str:
    return s[-amt:] + s[:-amt]

def move(s: str, src_pos: int, dst_pos: int) -> str:
    src = s[src_pos]
    list_ = list(s[:src_pos] + s[src_pos+1:])
    list_.insert(dst_pos, src)
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

cmds = [parse_cmd(line.strip()) for line in lines]
print(mutate(initial, cmds))

cmds = list(reversed(cmds))
print(mutate('decab', cmds))
