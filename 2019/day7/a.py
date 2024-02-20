from sys import argv
from itertools import permutations
import asyncio as aio

class Program:
    id = 0
    def __init__(self, program, input=None, output=None, seed=None):
        self.program = list(program)
        self.start = list(self.program)
        self.ip = 0
        self.input = input if input is not None else []
        self.output = output if output is not None else []
        self.seed = seed
        self.id = Program.id
        Program.id += 1
    
    def reset(self):
        self.program = list(self.start)
        self.ip = 0
        self.input.clear()
        self.output.clear()    
    
    def decode(n: int) -> (int, int, int):
        op = n % 100
        mode1 = n % 1000 // 100
        mode2 = n % 10000 // 1000
        return op, mode1, mode2

    def arg(self, a: int, mode: int) -> int:
        if mode == 0:
            return self.program[a]
        return a

    async def get_input(self,):
        if self.seed is not None:
            seed = self.seed
            self.seed = None
            return seed
        while len(self.input) == 0:
            await aio.sleep(0.01)
        return self.input.pop(0)

    async def execute(self):
        while self.ip < len(self.program) and self.program[self.ip] != 99:
            op, mode1, mode2 = Program.decode(self.program[self.ip])
            a = self.arg(self.program[self.ip+1], mode1)
            if op not in (3, 4):
                b = self.arg(self.program[self.ip+2], mode2)
            if op in (1, 2, 7, 8):
                if op == 1:
                    result = a + b
                elif op == 2:
                    result = a * b
                elif op == 7:
                    result = int(a < b)
                elif op == 8:
                    result = int(a == b)
                self.program[self.program[self.ip+3]] = result
                self.ip += 4
            elif op in (3, 4):
                if op == 3:
                    self.program[self.program[self.ip+1]] = await self.get_input()
                else:
                    self.output.append(a)
                self.ip += 2
            elif op in (5, 6):
                if op == 5:
                    if a != 0:
                        self.ip = b
                    else:
                        self.ip += 3
                else:
                    if a == 0:
                        self.ip = b
                    else:
                        self.ip += 3
            else:
                raise ValueError(op, self.program[self.ip])

async def execute_sequence(commands: [int], seq: [int]) -> int:
    output = []
    input = [0]
    for s in seq:
        program = Program(list(commands), [s] + input, output)
        await program.execute()
        input[0] = output[0]
        output.clear()
    return input[-1]

async def find_max_thrust(commands: [int]):
    max_ = 0
    for perm in permutations(range(5)):
        cur = await execute_sequence(commands, perm)
        if cur > max_:
            max_ = cur
    print(max_)
        
async def feedback(commands: [int], seq: [int]) -> int:
    programs = [None] * len(seq)
    buffers = [[], [], [], [], [], []]
    for i, s in enumerate(seq):
        programs[i] = Program(commands, buffers[i], buffers[(i+1) % len(seq)], s)
    tasks = [aio.create_task(program.execute()) for program in programs]
    buffers[0].append(0)
    for task in tasks:
        await task
    return buffers[0][-1]

async def find_max_feedback(commands: [int]):
    max_feedback = 0
    for perm in permutations(range(5, 10)):
        cur = await feedback(commands, perm)
        if cur > max_feedback:
            max_feedback = cur
    print(max_feedback)

commands = [int(token) for token in open(argv[1]).read().strip().split(',')]
aio.run(find_max_thrust(commands))
aio.run(find_max_feedback(commands))
