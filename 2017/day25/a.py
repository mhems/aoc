from sys import argv
from collections import namedtuple as nt

Action = nt('Action', ['write', 'left', 'next_state_name'])
State = nt('State', ['name', 'actions'])

with open(argv[1]) as fp:
    text = fp.read()

def parse_action(lines: [str]) -> Action:
    value = int(lines[0].split()[-1][-2])
    left = lines[1].split()[-1] == 'left.'
    next = lines[2].split()[-1][:-1]
    return Action(value, left, next)

def parse_state(text: str) -> (str, State):
    lines = text.split('\n')
    name = lines[0].split()[-1][:-1]
    actions = [parse_action(lines[2:5]), parse_action(lines[6:9])]
    return name, State(name, actions)

def parse(text: str) -> (State, int, {str: State}):
    paragraphs = text.split('\n\n')
    first_lines = paragraphs[0].split('\n')
    start_state_name = first_lines[0].split()[-1][:-1]
    n = int(first_lines[1].split()[-2])
    states = {}
    for paragraph in paragraphs[1:]:
        name, state = parse_state(paragraph)
        states[name] = state
    return states[start_state_name], n, states

def step(tape: [int], cursor: int, state: State, resize_factor=100) -> (str, [int], int):
    cur_value = tape[cursor]
    action = state.actions[cur_value]
    tape[cursor] = action.write
    if action.left:
        if cursor == 0:
            tape = ([0] * resize_factor) + tape
            cursor = resize_factor
        cursor -= 1
    else:
        if cursor == len(tape) - 1:
            tape += [0] * resize_factor
        cursor += 1
    return action.next_state_name, tape, cursor

def tape_str(tape: [int], cursor: int) -> str:
    before = ' '.join(map(str, tape[:cursor]))
    cur = ' [%d] ' % tape[cursor]
    after = ' '.join(map(str, tape[cursor + 1:]))
    return before + cur + after

def simulate(start_state, n, states) -> int:
    cursor, tape = n//2, [0] * n
    state = start_state
    for i in range(n):
        next_state_name, tape, cursor = step(tape, cursor, state)
        state = states[next_state_name]
        #print(tape_str(tape, cursor), 'after', i+1, 'steps, about to run', state.name)
    return sum(int(e == 1) for e in tape)

start_state, n, states = parse(text)
checksum = simulate(start_state, n, states)
print(checksum)
