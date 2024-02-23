from sys import argv
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
        self.base = 0
        self.memory = {}
        self.id = Program.id
        Program.id += 1
    
    def reset(self):
        self.program = list(self.start)
        self.memory = {}
        self.ip = 0
        self.input.clear()
        self.output.clear()    
    
    def decode(n: int) -> (int, int, int, int):
        op = n % 100
        mode1 = n % 1000 // 100
        mode2 = n % 10000 // 1000
        mode3 = n % 100000 // 10000
        return op, mode1, mode2, mode3

    def arg(self, a: int, mode: int) -> int:
        if mode == 0:
            return self.read(a)
        elif mode == 1:
            return a
        elif mode == 2:
            return self.read(a + self.base)
    
    def write_arg(self, a: int, mode: int) -> int:
        if mode == 0:
            return a
        elif mode == 1:
            raise ValueError()
        elif mode == 2:
            return a + self.base

    async def get_input(self,):
        if self.seed is not None:
            seed = self.seed
            self.seed = None
            return seed
        while len(self.input) == 0:
            await aio.sleep(0.01)
        return self.input.pop(0)

    def read(self, address) -> int:
        if address < len(self.program):
            return self.program[address]
        if address not in self.memory:
            self.memory[address] = 0
        return self.memory[address]
    
    def write(self, address, value):
        if address < len(self.program):
            self.program[address] = value
        else:
            self.memory[address] = value

    async def execute(self):
        while self.ip < len(self.program) and self.read(self.ip) != 99:
            op, mode1, mode2, mode3 = Program.decode(self.read(self.ip))
            a = self.arg(self.read(self.ip + 1), mode1)
            if op not in (3, 4, 9):
                b = self.arg(self.read(self.ip + 2), mode2)
            if op in (1, 2, 7, 8):
                if op == 1:
                    result = a + b
                elif op == 2:
                    result = a * b
                elif op == 7:
                    result = int(a < b)
                elif op == 8:
                    result = int(a == b)
                addr = self.write_arg(self.read(self.ip + 3), mode3)
                self.write(addr, result)
                self.ip += 4
            elif op in (3, 4):
                if op == 3:
                    input = await self.get_input()
                    addr = self.write_arg(self.read(self.ip + 1), mode1)
                    self.write(addr, input)
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
            elif op == 9:
                self.base += a
                self.ip += 2
            else:
                raise ValueError(op, self.program[self.ip])

async def part1(commands: [int]):
    output = []
    program = Program(commands, [], output)
    task = aio.create_task(program.execute())
    await task
    print(sum(int(output[i+2] == 2) for i in range(0, len(output), 3)))

def make_screen(output: [int]) -> ([[int]], (int, int), (int, int)):
    map = {}
    for _ in range(0, 2664 + 1, 3):
        x, y, tile = output.pop(0), output.pop(0), output.pop(0)
        if x != -1:
            map[(y, x)] = tile
    xs = [x for _, x in map.keys()]
    ys = [y for y, _ in map.keys()]
    minX, maxX = min(xs), max(xs)
    minY, maxY = min(ys), max(ys)
    screen = [[' '] * (maxX - minX + 1) for _ in range(maxY - minY + 1)]
    ball = None
    paddle = None
    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            screen[y][x] = map.get((y, x), 0)
            if screen[y][x] == 3:
                paddle = (y, x)
            elif screen[y][x] == 4:
                ball = (y, x)
    return screen, ball, paddle

def print_screen(screen: [[str]]):
    for row in screen:
        for cell in row:
            print(' #=-*'[cell], end='')
        print()
    print(flush=True)

async def part2(commands: [int]):
    input = []
    output = []
    commands[0] = 2
    program = Program(commands, input, output)
    task = aio.create_task(program.execute())
    while len(output) < 2667:
        await aio.sleep(0.01)
    screen, ball, paddle = make_screen(output)
    while not task.done():
        while len(output) > 0 and output[-1] != 4:
            await aio.sleep(0.01)
        for _ in range(0, len(output), 3):
            x, y, tile = output.pop(0), output.pop(0), output.pop(0)
            if x != -1:
                screen[y][x] = tile
                if tile == 4:
                    ball = (y, x)
                elif tile == 3:
                    paddle = (y, x)
        delta = ball[1] - paddle[1]
        input.append(delta//abs(delta) if delta else 0)
        await aio.sleep(0.01)
    print(output[-1])

commands = [int(token) for token in open(argv[1]).read().strip().split(',')]
aio.run(part1(commands))
aio.run(part2(commands))
