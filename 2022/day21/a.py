from sys import argv
from operator import add, sub, mul, floordiv, eq
import asyncio as aio

def parse() -> dict:
    d = dict()
    for line in open(argv[1]).readlines():
        tokens = line.strip().split(': ')
        if tokens[1][0].isdigit():
            d[tokens[0]] = int(tokens[1])
        else:
            d[tokens[0]] = tokens[1].split()
    return d

spoken = dict()

async def get_number(monkey: str) -> int:
    while monkey not in spoken:
        await aio.sleep(0.001)
    return spoken[monkey]

async def perform(monkey: str, action: (str, str, str)):
    a, op, b = action
    funcs = {'+': add, '-': sub, '*': mul, '/': floordiv, '==': eq}
    v1 = await get_number(a)
    v2 = await get_number(b)
    result = funcs[op](v1, v2)
    spoken[monkey] = result
    return result

async def yell(mapping: dict):
    tasks = []
    for monkey, action in mapping.items():
        if isinstance(action, int):
            spoken[monkey] = action
        else:
            tasks.append(aio.create_task(perform(monkey, action)))
    for task in tasks:
        await task

def update(i: int):
    spoken.clear()
    a, _, b = mapping['root']
    mapping['root'] = a, '==', b
    mapping['humn'] = i

def trial(mapping: dict, i: int) -> bool:
    update(i)
    aio.run(yell(mapping))
    a, _, b = mapping['root']
    #print(i, spoken['root'], spoken[a], 'vs', spoken[b])
    return spoken['root']

def find_equality(mapping: dict) -> int:
    i = 3582317956025
    while True:
        if trial(mapping, i):
            return i
        i += 1

mapping = parse()
aio.run(yell(mapping))
print(spoken['root'])
print(find_equality(mapping))
