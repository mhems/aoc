import sys
from typing import Iterable
from collections import deque, namedtuple as nt

# type { 0: vacant, 1 - 4: 'A' - 'D' }
# pods ordered top to bottom
# ready is True if no non-type pods in the Room
Room = nt('Room', 'type pods ready num_placed complete')
Position = nt('Position', 'ledges rooms size')
State = nt('State', 'position num_done energy')

lines = [line.strip().replace('#', '') for line in open(sys.argv[1]).readlines()[2:4]]

def build_initial_state(part1: bool = True) -> State:
    rows = lines if part1 else (lines[0], 'DCBA', 'DBAC', lines[1])
    rooms = tuple(Room(v + 1,
                       tuple(ord(row[v]) - ord('A') + 1 for row in rows),
                       False, 0, False)
                  for v in range(4))
    scored_rooms = tuple(score_room(room) for room in rooms)
    position = Position((0, 0, 0, 0, 0, 0, 0), scored_rooms, 2 if part1 else 4)
    return State(position, False, 0)

def score_room(room: Room) -> Room:
    num_placed = 0
    ready = True
    bottom = room.pods[len(room.pods) - 1]
    top = room.pods[0]
    if bottom == room.type:
        num_placed += 1
        if top == room.type:
            num_placed += 1
        if top != 0:
            ready = False
    elif bottom != 0:
        ready = False
    return Room(room.type, room.pods, ready, num_placed, False)

energy = {1: 1, 2: 10, 3: 100, 4: 1000}
def energy_required(type: int, amt: int) -> int:
    return energy[type] * amt

ledge_distances = {
    0: (3, 5, 7, 9),
    1: (2, 4, 6, 8),
    
    2: (2, 2, 4, 6),
    3: (4, 2, 2, 4),
    4: (6, 4, 2, 2),
    
    5: (8, 6, 4, 2),
    6: (9, 7, 5, 3)
}
room_distances = {
    0: (0, 4, 6, 8),
    1: (4, 0, 4, 6),
    2: (6, 4, 0, 4),
    3: (8, 6, 4, 0)
}
def compute_lower_bound(position: Position) -> int:
    energy = 0
    for i, ledge in enumerate(position.ledges):
        if ledge != 0:
            energy += energy_required(ledge, ledge_distances[i][ledge-1])
    for i, room in enumerate(position.rooms):
        blocker = False
        if not room.complete:
            num_diff = 0
            for j in range(len(room.pods) - room.num_placed - 1, -1, -1):
                cur = room.pods[j]
                if cur == 0:
                    break
                if cur != room.type:
                    blocker = True
                    energy += energy_required(cur, room_distances[room.type-1][room.pods[j]-1] + j)
                    num_diff += 1
                elif blocker: # types match but there is a non-match below us
                    num_diff += 1
                    energy += energy_required(cur, 4 + 2*j)
            extra = energy_required(room.type, max(num_diff - 1, 0))
            if extra > 0:
                energy += extra
    return energy

def yield_targets_from(index: int, left: bool, state: State) -> Iterable[tuple[int, int | Room]]:
    ledges, rooms, _ = state.position
    elements = [(0, ledges[0]), (1, ledges[1]),
                (0, rooms[0]), (2, ledges[2]), (1, rooms[1]), (3, ledges[3]), (2, rooms[2]), (4, ledges[4]), (3, rooms[3]),
                (5, ledges[5]), (6, ledges[6])]
    
    if left:
        # don't consider going from outer right to inner right
        if index >= 9:
            elements.pop()
            elements.pop()
        else:
            elements = elements[:index]
    else:
        # don't consider going from outer left to inner left
        if index <= 1:
            elements.pop(0)
            elements.pop(0)
        else:
            elements = elements[index+1:]
    
    if 1 <= index <= 9 or (index == 0 and ledges[1] == 0) or (index == 10 and ledges[5] == 0):
        iterable = reversed(elements) if left else elements
        for i, e in iterable:
            if isinstance(e, int):
                if e != 0:
                    # stop everything if hall is blocked
                    break
            elif not e.ready or e.complete:
                # skip rooms that cannot receive pods
                continue
            yield i, e

def ledge_index_to_global_index(ledge_index: int) -> int:
    if ledge_index <= 1:
        return ledge_index
    if ledge_index >= 5:
        return ledge_index + 4
    return 2*ledge_index - 1

def move_pod(room_index: int, rooms: tuple[Room], floor_index: int, new_value: int, ready: bool, added: bool, complete: bool) -> list[Room]:
    room = rooms[room_index]
    new_pods = list(room.pods)
    new_pods[floor_index] = new_value
    new_rooms = list(rooms)
    new_rooms[room_index] = Room(room.type, tuple(new_pods), ready, room.num_placed + int(added), complete)
    return new_rooms

ledge_to_room = {
    0: [3, 2, 2, 4, 6, 8, 9],
    1: [5, 4, 2, 2, 4, 6, 7],
    2: [7, 6, 4, 2, 2, 4, 5],
    3: [9, 8, 6, 4, 2, 2, 3]
}
def make_state(new_rooms: list[Room], new_ledges: list[int], prev: State, room_index: int,
               ledge_index: int, adder: int, src_type: int, room_done: bool) -> State:
    new_position = Position(tuple(new_ledges), tuple(new_rooms), prev.position.size)
    distance = ledge_to_room[room_index][ledge_index] + adder
    new_energy = prev.energy + energy_required(src_type, distance)
    return State(new_position, prev.num_done + int(room_done), new_energy)

def get_possible_transitions_from_ledge_to_room(ledge_index: int, left: bool, state: State) -> Iterable[State]:
    ledges, rooms, size = state.position
    src_type = ledges[ledge_index]
    for dest_idx, value in yield_targets_from(ledge_index_to_global_index(ledge_index), left, state):
        if isinstance(value, Room) and value.type == src_type:
            new_ledges = list(ledges)
            new_ledges[ledge_index] = 0
            room_done = value.num_placed + 1 == size
            new_rooms = move_pod(dest_idx, rooms, size - value.num_placed - 1, src_type, True, True, room_done)
            yield make_state(new_rooms, new_ledges, state, dest_idx, ledge_index, size - 1 - value.num_placed, src_type, room_done)

def get_possible_transitions_from_room_to_ledge(room_index: int, left: bool, state: State) -> Iterable[State]:
    ledges, rooms, _ = state.position
    src_room = rooms[room_index]
    for i, v in enumerate(src_room.pods):
        if v != 0:
            src_type = v
            break
    ready = True
    for v in src_room.pods[i+1:]:
        if v != 0 and v != src_room.type:
            ready = False
            break
    for dest_idx, value in yield_targets_from(2 + room_index * 2, left, state):
        if isinstance(value, int):
            new_ledges = list(ledges)
            new_ledges[dest_idx] = src_type
            new_rooms = move_pod(room_index, rooms, i, 0, ready, False, False)
            yield make_state(new_rooms, new_ledges, state, room_index, dest_idx, i, src_type, False)

def get_possible_transitions(state: tuple[int]) -> Iterable[State]:
    ledges, rooms, _ = state.position
    for i, ledge in enumerate(ledges):
        if ledge != 0:
            if i > 0:
                yield from get_possible_transitions_from_ledge_to_room(i, True, state)
            if i < 6:
                yield from get_possible_transitions_from_ledge_to_room(i, False, state)
    for i, room in enumerate(rooms):
        if not room.ready and not room.complete:
            yield from get_possible_transitions_from_room_to_ledge(i, True, state)
            yield from get_possible_transitions_from_room_to_ledge(i, False, state)

def find_minimum(part1: bool = True) -> int:
    q = deque([build_initial_state(part1)])
    visited = dict()
    best = 1_000_000
    while q:
        state = q.popleft()
        if state.num_done == 4:
            if state.energy < best:
                best = state.energy
                print(f'new best: {state.energy}', flush=True)
        else:
            lower_bound = state.energy + compute_lower_bound(state.position)
            existing_energy = visited.get(state.position, None)
            if existing_energy is not None:
                if lower_bound >= existing_energy:
                    continue
                else:
                    visited[state.position] = min(existing_energy, lower_bound)
            else:
                visited[state.position] = lower_bound
            if lower_bound < best:
                for next in get_possible_transitions(state):
                    q.append(next)
    return best

print('answer', find_minimum())
print('answer', find_minimum(False))
