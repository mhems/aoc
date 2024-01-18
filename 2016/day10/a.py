from sys import argv
from collections import namedtuple as nt
import asyncio as aio

Literal = nt('Literal', ['value', 'rx'])
Receiver = nt('Receiver', ['is_bot', 'num'])
Give = nt('Give', ['tx', 'low', 'high'])
Instruction = nt('Instruction', ['is_give', 'value'])

mailboxes = {}
comparisons = {}
outputs = {}

with open(argv[1]) as fp:
    lines = fp.readlines()

def parse_literal(s: str) -> Literal:
    tokens = s.strip().split()
    return Literal(int(tokens[1]), parse_receiver(tokens[-2], tokens[-1]))

def parse_receiver(word: str, num: str) -> Receiver:
    return Receiver(word == 'bot', int(num))

def parse_give(s: str) -> Give:
    tokens = s.strip().split()
    return Give(int(tokens[1]),
                parse_receiver(tokens[5], tokens[6]),
                parse_receiver(tokens[-2], tokens[-1]))

def parse_line(s: str):
    if s.startswith('value'):
        return Instruction(False, parse_literal(s))
    return Instruction(True, parse_give(s))

def give(value: int, receiver: Receiver):
    if receiver.is_bot:
        if receiver.num not in mailboxes:
            mailboxes[receiver.num] = []
        mailboxes[receiver.num].append(value)
    else:
        if receiver.num not in outputs:
            outputs[receiver.num] = []
        outputs[receiver.num].append(value)

async def process_instruction(instruction):
    if not instruction.is_give:
        give(instruction.value.value, instruction.value.rx)
    else:
        tx = instruction.value.tx
        while tx not in mailboxes or len(mailboxes[tx]) < 2:
            await aio.sleep(0.01)
        low, high = min(mailboxes[tx]), max(mailboxes[tx])
        give(low, instruction.value.low)
        give(high, instruction.value.high)
        comparisons[tx] = (low, high)

async def process_instructions(instructions):
    tasks = [aio.create_task(process_instruction(i)) for i in instructions]
    for task in tasks:
        await task

instructions = [parse_line(line.strip()) for line in lines]
aio.run(process_instructions(instructions))

print(outputs)
#print(comparisons)

for bot, (low, high) in comparisons.items():
    if low == 17 and high == 61:
        print(bot)
        
print(outputs[0][0] * outputs[1][0] * outputs[2][0])