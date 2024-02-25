from sys import argv
import asyncio as aio
from collections import deque

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
            await aio.sleep(0.001)
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

def output_grid(walls, visited, target, filename):
    all = walls.union(visited)
    xs = [x for _, x in all]
    ys = [y for y, _ in all]
    minX, maxX = min(xs), max(xs)
    minY, maxY = min(ys), max(ys)
    with open(filename, 'w') as fp:
        for y in range(minY, maxY + 1):
            for x in range(minX, maxX + 1):
                if (y, x) in walls:
                    fp.write('#')
                elif (y, x) in visited:
                    if y == target[0] and x == target[1]:
                        fp.write('O')
                    else:
                        fp.write('.')
                else:
                    fp.write(' ')
            fp.write('\n')

async def bfs(commands: [int]):
    input = []
    output = []
    async def move(direction: int) -> int:
        assert len(output) == 0
        input.append(direction)
        while len(output) < 1:
            await aio.sleep(0.001)
        return output.pop(0)
    aio.create_task(Program(commands, input, output).execute())
    q = deque()
    visited = set()
    walls = set()
    q.append(((0, 0), []))
    visited.add((0, 0))
    retrace = {0: 1, 1: 0, 2: 3, 3: 2}
    target = None
    distance = None
    while len(q) > 0:
        pos, history = q.popleft()
        for step in history:
            await move(step)
        for i, direction in enumerate(((-1, 0), (1, 0), (0, -1), (0, 1))):
            new_pos = (pos[0] + direction[0], pos[1] + direction[1])
            result = await move(i + 1)
            if result == 2:
                distance = len(history) + 1
                target = new_pos
            elif result == 0:
                walls.add(new_pos)
            if result != 0:
                result = await move(retrace[i] + 1)
                assert result == 1 or target is not None
                if new_pos not in visited:
                    visited.add(new_pos)
                    q.append((new_pos, history + [i+1]))
        # backtrack back to pos
        for step in reversed(history):
            await move(retrace[step - 1] + 1)
    output_grid(walls, visited, target, 'grid.txt')
    return distance

commands = [int(token) for token in open(argv[1]).read().strip().split(',')]
print(aio.run(bfs(commands)))
