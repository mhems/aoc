from sys import argv
from collections import namedtuple as nt

Op = nt('Op', ['label', 'hash', 'op', 'arg'])
Lens = nt('Lens', ['label', 'length'])

def hash(s: str) -> int:
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val %= 256
    return val

with open(argv[1]) as fp:
    line = fp.readlines()[0].strip()
cmds = line.split(',')
answer = sum(hash(cmd) for cmd in cmds)
print(answer)

def parse_op(s: str) -> Op:
    if '=' in s:
        label, value = s.split('=')
        return Op(label, hash(label), '=', int(value))
    elif '-' in s:
        label = s[:-1:]
        return Op(label, hash(label), '-', None)
    
def box_focal_power(box: [Lens], index: int) -> int:
    '''return sum of power of all lens' in box'''
    return sum((index+1) * (i+1) * lens.length for i, lens in enumerate(box))

boxes = [list() for _ in range(256)]
ops = list(map(parse_op, cmds))
for op in ops:
    box = boxes[op.hash]
    if op.op == '-':
        for lens in box:
            if lens.label == op.label:
                box.remove(lens)
                break
    elif op.op == '=':
        for i, lens in enumerate(box):
            if lens.label == op.label:
                box[i] = Lens(lens.label, op.arg)
                break
        else:
            box.append(Lens(op.label, op.arg))

answer = sum(box_focal_power(box, i) for i, box in enumerate(boxes))
print(answer)