from sys import argv
from collections import namedtuple as nt
from collections import deque
from math import lcm

Module = nt('Module', ['prefix', 'name', 'destinations'])

def parse_module(txt: str) -> Module:
    left, right = txt.strip().split(' -> ')
    prefix = left[0]
    name = left[1:]
    if prefix not in '%&':
        prefix = None
        name = left
    return Module(prefix, name, right.split(', '))

def make_state(modules: {str: Module}) -> {str: bool}:
    state = {}
    for name, module in modules.items():
        if module.prefix == '%':
            state[name] = False
        elif module.prefix == '&':
            for other_name, other_module in modules.items():
                if name != other_name:
                    if any(n == name for n in other_module.destinations):
                        if name not in state:
                            state[name] = {}
                        state[name][other_name] = False
    return state

def trace(modules: {str: Module},
          state: dict,
          counts: dict,
          i: int,
          debug: bool = False) -> dict:
    pulse_counts = {True: 0, False: 1}
    q = deque()
    for destination in modules['broadcaster'].destinations:
        q.append((destination, False, 'broadcaster'))
    pulse_counts[False] += len(modules['broadcaster'].destinations)
    while len(q) > 0:
        name, high, from_ = q.popleft()
        if debug:
            print(name, 'got', high, 'from', from_)
        if name not in modules:
            continue
        module = modules[name]
        if module.prefix == '%':
            if not high:
                on = state[name]
                state[name] = not on
                for destination in module.destinations:
                    if debug:
                        print(' ', name, 'sending', not on, 'to', destination)
                    pulse_counts[not on] += 1
                    q.append((destination, not on, name))
                if debug:
                    print()
        elif module.prefix == '&':
            state[name][from_]= high
            send_high = not all(state[name].values())
            for destination in module.destinations:
                if debug:
                    print(' ', name, 'sending', send_high, 'to', destination)
                if send_high and destination == 'tg':
                    if name not in counts:
                        counts[name] = i + 1
                pulse_counts[send_high] += 1
                q.append((destination, send_high, name))
            if debug:
                print()
    return state, pulse_counts

def push_button(modules: {str: Module}, n: int = 1000) -> {str: bool}:
    state = make_state(modules)
    pulse_counts = {True: 0, False: 0}
    for _ in range(n):
        state, cur_counts = trace(modules, state, None, None)
        pulse_counts[True] += cur_counts[True]
        pulse_counts[False] += cur_counts[False]
    return pulse_counts[True] * pulse_counts[False]

def rx(modules: {str: Module}) -> int:
    state = make_state(modules)
    i = 0
    cycles = dict()
    while True:
        state, _ = trace(modules, state, cycles, i)
        i += 1
        if len(cycles) == 4:
            return lcm(*cycles.values())

with open(argv[1]) as fp:
    modules = [parse_module(line.strip()) for line in fp.readlines()]
module_map = {module.name: module for module in modules}
print(push_button(module_map))
print(rx(module_map))
