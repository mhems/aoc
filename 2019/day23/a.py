from sys import argv

inputs = None
nat_packet = None

def transmit(dest: int, pos: (int, int)):
    global inputs, nat_packet
    if dest == 255:
        nat_packet = pos
    else:
        inputs[dest].append(pos[0])
        inputs[dest].append(pos[1])

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
        self.idle = 0
        self.id = Program.id
        Program.id += 1

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

    def get_input(self,):
        if self.seed is not None:
            seed = self.seed
            self.seed = None
            return seed
        if len(self.input) == 0:
            return -1
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

    def step(self):
        if self.ip < len(self.program) and self.read(self.ip) != 99:
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
                    input = self.get_input()
                    if input == -1:
                        self.idle += 1
                    else:
                        self.idle = 0
                    addr = self.write_arg(self.read(self.ip + 1), mode1)
                    self.write(addr, input)
                else:
                    self.output.append(a)
                    if len(self.output) > 0 and len(self.output) % 3 == 0:
                        dest, x, y = self.output[-3:]
                        transmit(dest, (x, y))
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

def switch(commands: [int], num_cpus=50):
    global inputs, nat_packet
    inputs = [list() for _ in range(num_cpus)]
    outputs = [list() for _ in range(num_cpus)]
    nics = [Program(commands, inputs[i], outputs[i], i) for i in range(num_cpus)]
    prev_nat_packet = None
    sent_resume = False
    while True:
        for nic in nics:
            nic.step()
        if all(nic.idle > 100 for nic in nics):
            if nat_packet is not None:
                if prev_nat_packet is not None and nat_packet[1] == prev_nat_packet[1]:
                    print(nat_packet[1])
                    return
                if not sent_resume:
                    print(nat_packet[1])
                    sent_resume = True
                transmit(0, nat_packet)
                prev_nat_packet = nat_packet
                nat_packet = None

commands = [int(token) for token in open(argv[1]).read().strip().split(',')]
switch(commands)
