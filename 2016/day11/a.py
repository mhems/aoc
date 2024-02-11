from sys import argv
from collections import namedtuple as nt
from itertools import combinations
import heapq
from time import time

Component = nt('Component', ['chemical', 'chip'])
State = nt('State', ['elev', 'chips', 'gens', 'steps'])
Transition = nt('Transition', ['delta', 'pos_a', 'chip_a', 'pos_b', 'chip_b'])

count = 0
name_to_pos = {}
pos_to_name = {}

def parse_line(line: str) -> [Component]:
    rest = ' '.join(line.strip().split()[4:])[:-1]
    tokens = rest.split(', ')
    if len(tokens) > 1:
        tokens[-1] = tokens[-1][4:]
    def parse_component(text: [str]) -> Component:
        tokens = text.split()
        chip = tokens[-1] == 'microchip'
        chemical = tokens[1].split('-')[0] if chip else tokens[1]
        return Component(chemical, chip)
    return [parse_component(token) for token in tokens]

def make_state(factory: [[Component]]) -> State:
    global count, name_to_pos, pos_to_name
    chips, gens = [], []
    for floor in factory:
        chip = 0
        gen = 0
        for component in floor: 
            if component.chemical not in name_to_pos:
                name_to_pos[component.chemical] = count
                pos_to_name[count] = component.chemical
                count += 1
            v = name_to_pos[component.chemical]
            if component.chip:
                chip |= 1 << v
            else:
                gen |= 1 << v
        chips.append(chip)
        gens.append(gen)
    return State(0, tuple(chips), tuple(gens), 0)

def print_state(state: State):
    global count, pos_to_name
    for floor in range(len(state.chips) - 1, -1, -1):
        print('E' if floor == state.elev else ' ', end = ' | ')
        for pos in range(count - 1, -1, -1):
            has_chip = state.chips[floor] & (1 << pos)
            has_gen = state.gens[floor] & (1 << pos)
            if has_chip or has_gen:
                print(pos_to_name[pos].capitalize()[:2], end='')
                print('M' if has_chip else '-', end='')
                print('G' if has_gen else '-', end='')
            else:
                print(' ' * 4, end='')
            print('  ', end='')
        print()
    print()

def is_valid(state: State) -> bool:
    for chips, gens in zip(state.chips, state.gens):
        if gens != 0 and chips != 0 and chips ^ gens != 0:
            for pos in range(count - 1, -1, -1):
                if (chips &  (1 << pos) != 0 and # if there is a chip,
                    gens  &  (1 << pos) == 0 and # without a generator,
                    gens  & ~(1 << pos) != 0):   # and other generators exist
                    return False
    return True

def apply_transition(state: State, transition: Transition) -> State:
    elev, chips, gens = state.elev, list(state.chips), list(state.gens)
    new_elev = elev + transition.delta
    if transition.chip_a:
        chips[elev] &= ~(1 << transition.pos_a)
        chips[new_elev] |= (1 << transition.pos_a)
    else:
        gens[elev] &= ~(1 << transition.pos_a)
        gens[new_elev] |= (1 << transition.pos_a)
    if transition.pos_b is not None:
        if transition.chip_b:
            chips[elev] &= ~(1 << transition.pos_b)
            chips[new_elev] |= (1 << transition.pos_b)
        else:
            gens[elev] &= ~(1 << transition.pos_b)
            gens[new_elev] |= (1 << transition.pos_b)
    return State(new_elev, tuple(chips), tuple(gens), state.steps + 1)

def generate_contents_choice(gens: int, chips: int) -> [(int, bool, int, bool)]:
    global count
    chip_pos = []
    gen_pos = []
    for pos in range(count - 1, -1, -1):
        if gens & (1 << pos):
            gen_pos.append(pos)
        if chips & (1 << pos):
            chip_pos.append(pos)
    contents = [(p, True) for p in chip_pos] + [(p, False) for p in gen_pos]
    choices = list(tuple(a + b) for a, b in combinations(contents, 2))
    choices.extend((p, True, None, None) for p in chip_pos)
    choices.extend((p, False, None, None) for p in gen_pos)
    return choices            

def generate_transitions(state: State) -> [Transition]:
    transitions = []
    contents_choices = list(generate_contents_choice(state.gens[state.elev], state.chips[state.elev]))
    if state.elev < 4 - 1:
        transitions.extend(Transition(1, *choice) for choice in contents_choices)
    if state.elev > 0:
        transitions.extend(Transition(-1, *choice) for choice in contents_choices)
    return transitions

def is_goal_state(state: State) -> bool:
    return state.elev == 3 and all(chip + gen == 0 for chip, gen in zip(state.chips[:3], state.gens[:3]))

def remove_steps(state: State) -> (int, (int, int, int, int), (int, int, int, int)):
    return (state.elev, state.chips, state.gens)

def heuristic(state: State) -> int:
    def floor_empty(floor: int) -> bool:
        return state.chips[floor] == 0 and state.gens[floor] == 0
    def num_on_floor(floor: int) -> int:
        if floor_empty(floor):
            return 0
        num = 0
        for pos in range(count - 1, -1, -1):
            if state.chips[floor] & (1 << pos):
                num += 1
            if state.gens[floor] & (1 << pos):
                num += 1
        return num
    value = 100*state.steps - 10*num_on_floor(3) - num_on_floor(2)
    if floor_empty(0):
        value -= 10_000
        if floor_empty(1):
            value -= 100_000
            if floor_empty(2):
                value -= 1_000_000
    return value

def priority_bfs(state: State) -> int:
    q = []
    heapq.heappush(q, (0, state))
    visited = set()
    visited.add(remove_steps(state))
    start_time = time()
    while len(q) > 0:
        _, cur_state = heapq.heappop(q)
        if is_goal_state(cur_state):
            print('took', round(time() - start_time, 2), 'seconds')
            return cur_state.steps
        for transition in generate_transitions(cur_state):
            new_state = apply_transition(cur_state, transition)
            without_steps = remove_steps(new_state)
            if is_valid(new_state) and without_steps not in visited:
                visited.add(without_steps)
                heapq.heappush(q, (heuristic(new_state), new_state))

with open(argv[1]) as fp:
    lines = fp.readlines()

floors = [parse_line(line.strip()) for line in lines[:-1]] + [[]]
state = make_state(floors)
#print_state(state)
print(priority_bfs(state))

name_to_pos['elerium'] = count
name_to_pos['dilithium'] = count + 1
pos_to_name[count] = 'elerium'
pos_to_name[count + 1] = 'dilithium'
chips, gens = state.chips[0] | (3 << count), state.gens[0] | (3 << count)
count += 2
state = State(0, tuple([chips] + list(state.chips[1:])), tuple([gens] + list(state.gens[1:])), 0)
#print_state(state)
print(priority_bfs(state))
