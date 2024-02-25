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

def make_grid(output: [int]) -> [[str]]:
    grid = []
    i = 0
    while i < len(output):
        row = []
        while output[i] != ord('\n'):
            row.append(chr(output[i]))
            i += 1
        grid.append(row)
        i += 1
    return grid

def neighbors(pos: (int, int)) -> [(int, int)]:
    deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    return [(pos[0] + y, pos[1] + x) for y, x in deltas]

def find_intersections(grid: [[str]]) -> [(int, int)]:
    intersections = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if 0 < x < len(grid[0])-1 and 0 < y < len(grid)-1 and cell == '#':
                if all(grid[j][i] == '#' for j, i in neighbors((y, x))):
                    intersections.append((y, x))
    return intersections

async def draw(commands: [int]):
    output = []
    await Program(commands, [], output).execute()
    grid = make_grid(output)
    intersections = find_intersections(grid)
    print(sum(y * x for y, x in intersections))

def encode(commands: [str]) -> [str]:
    input = []
    for command in commands:
        for ch in command:
            input.append(ord(ch))
        input.append(ord('\n'))
    return input

async def vacuum(commands: [int]):
    commands[0] = 2
    directions = ['A,B,A,B,A,C,B,C,A,C', 'L,10,L,12,R,6', 'R,10,L,4,L,4,L,12', 'L,10,R,10,R,6,L,4', 'n']
    input = encode(directions)
    output = []
    await Program(commands, input, output).execute()
    print(output[-1])

commands = [int(token) for token in open(argv[1]).read().strip().split(',')]
aio.run(draw(commands))
aio.run(vacuum(commands))
