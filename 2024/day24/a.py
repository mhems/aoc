from sys import argv
import asyncio as aio
import pydot

class Gate:
    def __init__(self, text: str):
        tokens = text.strip().split()
        self.a = tokens[0]
        self.op = tokens[1]
        self.b = tokens[2]
        self.result = tokens[-1]
    
    @property
    def is_input(self) -> bool:
        return self.a[0] in 'xy' and self.b[0] in 'xy'

    @property
    def is_output(self) -> bool:
        return self.result[0] == 'z'

    @property
    def output_num(self) -> int:
        return int(self.result[1:]) if self.is_output else None

    def evaluate(self, a_value: int, b_value: int) -> int:
        self.a_value = a_value
        self.b_value = b_value
        if self.op == 'AND':
            self.result_value = a_value & b_value
        elif self.op == 'OR':
            self.result_value = a_value | b_value
        elif self.op == 'XOR':
            self.result_value = a_value ^ b_value
        return self.result_value
        
    def __str__(self) -> str:
        return f'{self.a} {self.op} {self.b} = {self.result}'

def parse_value(text: str) -> (str, int):
    tokens = text.strip().split(': ')
    return tokens[0], int(tokens[1])

def get_number(letter: str, values: {str, int}) -> int:
    keys = sorted({k for k in values.keys() if k.startswith(letter)},
                  key=lambda k: int(k[1:]),
                  reverse=True)
    return int(''.join(str(values[k]) for k in keys), base=2)   

def simulate(values: {str: int}, gates: [Gate]) -> int:
    async def get_input(wire: str) -> int:
        while wire not in values:
            await aio.sleep(0.01)
        return values[wire]
    async def evaluate(gate: Gate) -> int:
        operand1 = await get_input(gate.a)
        operand2 = await get_input(gate.b)
        values[gate.result] = gate.evaluate(operand1, operand2)
    async def do():
        tasks = [aio.create_task(evaluate(gate)) for gate in gates]
        for task in tasks:
            await task
    aio.run(do())
    return get_number('z', values)

def analysis(gates: [Gate]) -> str:
    src_to_gate = {(gate.op, tuple(sorted((gate.a, gate.b)))): gate for gate in gates}

    def find_gate_with_operand(operand: str) -> Gate:
        return {gate for gate in gates if gate.a == operand or gate.b == operand}

    def verify_half() -> (bool, str):
        xor_gate = src_to_gate[('XOR', ('x00', 'y00'))]
        and_gate = src_to_gate[('AND', ('x00', 'y00'))]
        if xor_gate.result != 'z00':
            return False, None
        return True, and_gate.result

    def verify_full(n: int, carry_in: str) -> (bool, str):
        num_str = f'{n:02}'
        inputs = ('x' + num_str, 'y' + num_str)
        input_xor_gate = src_to_gate[('XOR', inputs)]
        input_and_gate = src_to_gate[('AND', inputs)]
        intermediate_gates = find_gate_with_operand(input_xor_gate.result)
        
        if len(intermediate_gates) != 2:
            return False, None
        
        a, b = intermediate_gates
        if a.op == 'AND':
            intermediate_and, intermediate_xor = a, b
        else:
            intermediate_and, intermediate_xor = b, a

        if intermediate_xor.a == input_xor_gate.result:
            if carry_in and intermediate_xor.b != carry_in:
                return False, None
        elif intermediate_xor.b == input_xor_gate.result:
            if carry_in and intermediate_xor.a != carry_in:
                return False, None
        else:
            return False, None
        
        if intermediate_xor.result[0] != 'z' or intermediate_xor.output_num != n:
            return False, None
        
        if intermediate_and.a == input_xor_gate.result:
            if carry_in and intermediate_and.b != carry_in:
                return False, None
        elif intermediate_and.b == input_xor_gate.result:
            if carry_in and intermediate_and.a != carry_in:
                return False, None
        else:
            return False, None
        
        intermediate_ors = find_gate_with_operand(input_and_gate.result)
        if len(intermediate_ors) != 1:
            return False, None
        intermediate_or = next(iter(intermediate_ors))
        if intermediate_or.op != 'OR':
            return False, None
        elif intermediate_or.a == input_and_gate.result:
            if intermediate_or.b != intermediate_and.result:
                return False, None
        elif intermediate_or.a == intermediate_and.result:
            if intermediate_or.b != input_and_gate.result:
                return False, None

        return True, intermediate_or.result
        
    ok, carry = verify_half()
    if not ok:
        print('look at z00')
        carry = None
    for i in range(1, 45):
        ok, carry = verify_full(i, carry)
        if not ok:
            print(f'look at z{i:02}')
            carry = None
    if carry != 'z45':
        print('look at z45')

def make_graph(gates: [Gate]):
    def make_node(name: str) -> pydot.Node:
        if name[0] in 'xyz':
            shape = "square"
            color = 'blue' if name[0] == 'z' else 'green'
        else:
            shape = 'circle'
            color = 'violet'
        return pydot.Node(name, shape=shape, style='filled', fillcolor=color)
    graph = pydot.Dot('my_graph', graph_type='digraph')
    i = 0
    for gate in gates:
        a_node = make_node(gate.a)
        b_node = make_node(gate.b)
        c_node = make_node(gate.result)
        if gate.op == 'AND':
            shape = 'house'
            color = 'red'
        elif gate.op == 'OR':
            shape = 'triangle'
            color = 'orange'
        else:
            shape = 'trapezium'
            color = 'yellow'
        op_node = pydot.Node(str(i), label=gate.op, shape=shape, style='filled', fillcolor=color)
        i += 1
        graph.add_node(a_node)
        graph.add_node(b_node)
        graph.add_node(c_node)
        graph.add_node(op_node)
        graph.add_edge(pydot.Edge(a_node, op_node))
        graph.add_edge(pydot.Edge(b_node, op_node))
        graph.add_edge(pydot.Edge(op_node, c_node))
    graph.write_png('circuit.png')

values, gates = open(argv[1]).read().split('\n\n')
values = dict(parse_value(value) for value in values.split('\n'))
gates = [Gate(gate) for gate in gates.strip().split('\n')]
print(simulate(values, gates), flush=True)
make_graph(gates)
analysis(gates)
