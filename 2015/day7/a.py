from sys import argv
import asyncio as aio

with open(argv[1]) as fp:
    lines = fp.readlines()

circuit: {str: int} = {}

async def handle_arg(arg: str) -> int:
    try:
        return int(arg)
    except ValueError:
        while arg not in circuit:
            await aio.sleep(0.01)
        return circuit[arg]    

async def apply_step(line: str):
    tokens = line.strip().split()
    out = tokens[-1]
    if tokens[0] == 'NOT':
        val = await handle_arg(tokens[1])
        circuit[out] = ~val % (2**16)
    elif len(tokens) < 4:
        val = await handle_arg(tokens[0])
        circuit[out] = val
    elif tokens[1] == 'AND':
        a = await handle_arg(tokens[0])
        b = await handle_arg(tokens[2])
        circuit[out] = a & b
    elif tokens[1] == 'OR':
        a = await handle_arg(tokens[0])
        b = await handle_arg(tokens[2])
        circuit[out] = a | b
    elif tokens[1] == 'LSHIFT':
        val = await handle_arg(tokens[0])
        circuit[out] = val << int(tokens[2])
    elif tokens[1] == 'RSHIFT':
        val = await handle_arg(tokens[0])
        circuit[out] = val >> int(tokens[2])

async def apply_steps(lines: [str]):
    tasks = [aio.create_task(apply_step(line)) for line in lines]
    for task in tasks:
        await task

aio.run(apply_steps(lines))

if 'a' in circuit:
    print(circuit['a'])
else:
    print(circuit)
