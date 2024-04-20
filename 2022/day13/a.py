from sys import argv
from functools import cmp_to_key

def parse() -> [(list, list)]:
    chunks = open(argv[1]).read().split('\n\n')
    pairs = []
    for chunk in chunks:
        pairs.append(tuple(eval(line.strip()) for line in chunk.strip().split('\n')))
    return pairs

def compare(a, b) -> int:
    for left, right in zip(a, b):
        left_is_list = isinstance(left, list)
        right_is_list = isinstance(right, list)
        if left_is_list and right_is_list:
            if r := compare(left, right):
                return r
        elif not left_is_list and not right_is_list:
            if right < left:
                return -1
            if left < right:
                return 1
        elif left_is_list:
            if r := compare(left, [right]):
                return r
        else:
            if r := compare([left], right):
                return r
    if len(b) < len(a):
        return -1
    if len(a) < len(b):
        return 1
    return 0

pairs = parse()
print(sum(i+1 for i, (a, b) in enumerate(pairs) if compare(a, b) == 1))
packets = [packet for pair in pairs for packet in pair]
packets.append([[2]])
packets.append([[6]])
in_order = sorted(packets, key=cmp_to_key(compare), reverse=True)
print((in_order.index([[2]]) + 1) * (in_order.index([[6]]) + 1))
