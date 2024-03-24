from sys import argv
from collections import namedtuple as nt
from math import prod
from operator import lt, gt, eq

Packet = nt('Packet', ['version', 'type', 'packet'])
Literal = nt('Literal', ['value'])
Operator = nt('Operator', ['packets'])

def parse_literal(s: str) -> (Literal, int):
    pos = 0
    bitstr = ''
    group = s[pos: pos+5]
    while group[0] == '1':
        bitstr += group[1:]
        pos += 5
        group = s[pos: pos+5]
    bitstr += group[1:]
    pos += 5
    return Literal(int(bitstr, 2)), pos

def parse_operator(s: str) -> (Operator, int):
    pos = 1
    packets = []
    if s[0] == '0':
        total_length = int(s[1:16], 2)
        pos += 15
        while pos - 16 < total_length:
            packet, end = parse_packet(s[pos:])
            packets.append(packet)
            pos += end
    else:
        num_packets = int(s[1:12], 2)
        pos += 11
        while len(packets) < num_packets:
            packet, end = parse_packet(s[pos:])
            packets.append(packet)
            pos += end
    return Operator(packets), pos

def parse_packet(s: str) -> (Packet, int):
    version = int(s[:3], 2)
    type_ = int(s[3:6], 2)
    pos = 6
    if type_ == 4:
        packet, end = parse_literal(s[6:])
        pos += end
    else:
        packet, end = parse_operator(s[6:])
        pos += end
    return Packet(version, type_, packet), pos

def version_sum(packet: Packet) -> int:
    if isinstance(packet, Literal):
        return 0
    elif isinstance(packet, Operator):
        return sum(version_sum(p) for p in packet.packets)
    elif isinstance(packet, Packet):
        return packet.version + version_sum(packet.packet)

def evaluate(packet: Packet) -> int:
    if packet.type == 4:
        return packet.packet.value
    else:
        op = {0: sum, 1: prod, 2: min, 3: max, 5: gt, 6: lt, 7: eq}
        func = op[packet.type]
        args = [evaluate(arg) for arg in packet.packet.packets]
        if packet.type >= 5:
            return int(func(*args))
        return func(args)

for line in open(argv[1]).readlines():
    packet, _ = parse_packet(bin(int('1' + line.strip(), 16))[3:])
    print(version_sum(packet), evaluate(packet))
