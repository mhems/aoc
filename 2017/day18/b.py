from sys import argv
from collections import namedtuple as nt
from operator import mul, mod
import asyncio as aio 

Op = nt('Op', ['name', 'args'])
State = nt('State', ['regs', 'pc', 'queue', 'num_sends'])

with open(argv[1]) as fp:
    lines = fp.readlines()

def parse_arg(arg):
    try:
        return int(arg)
    except ValueError:
        return arg

def parse_op(line: str) -> Op:
    tokens = line.strip().split()
    return Op(tokens[0], [parse_arg(arg) for arg in tokens[1:]])

async def poll(queue: [int], timeout: float) -> int:
    async with aio.timeout(timeout):
        while len(queue) == 0:
            await aio.sleep(0.01)
        return queue.pop(0)

async def run_op(state: State, op: Op, other_state: State, timeout: float) -> State:
    def lookup(arg):
        if isinstance(arg, int):
            return arg
        if arg not in state.regs:
            state.regs[arg] = 0
        return state.regs[arg]
    num_sends = state.num_sends
    if op.name == 'jgz':
        if lookup(op.args[0]) > 0:
            pc = state.pc + lookup(op.args[1])
        else:
            pc = state.pc + 1
    else:
        if op.name == 'set':
            state.regs[op.args[0]] = lookup(op.args[1])
        elif op.name == 'add':
            state.regs[op.args[0]] = sum(map(lookup, op.args))
        elif op.name == 'mul':
            state.regs[op.args[0]] = mul(*map(lookup, op.args))
        elif op.name == 'mod':
            state.regs[op.args[0]] = mod(*map(lookup, op.args))
        elif op.name == 'snd':
            other_state.queue.append(lookup(op.args[0]))
            num_sends += 1
        elif op.name == 'rcv':
            state.regs[op.args[0]] = await poll(state.queue, timeout)
        pc = state.pc + 1
    return State(state.regs, pc, state.queue, num_sends)

async def run(state: State, ops: [Op], other_state: State, timeout: float):
    try:
        while state.pc < len(ops):
            state = await run_op(state, ops[state.pc], other_state, timeout)
    except aio.TimeoutError as e:
        pass
    return state.num_sends

async def run_two(ops: [Op], timeout: float) -> int:
    state_0 = State({'p': 0}, 0, [], 0)
    state_1 = State({'p': 1}, 0, [], 0)
    task0 = aio.create_task(run(state_0, ops, state_1, timeout))
    task1 = aio.create_task(run(state_1, ops, state_0, timeout))
    await task0
    print('0', state_0.regs)
    print('1', state_1.regs)
    return await task1

ops = [parse_op(line.strip()) for line in lines]
answer = aio.run(run_two(ops, 5))
print(answer)
