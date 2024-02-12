from sys import argv
from itertools import takewhile
from collections import deque

def adjacent_positions(pos: (int, int), grid: [[str]]):
    '''return list of adjacent positions in reading order'''
    deltas = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    X, Y = len(grid[0]), len(grid)
    return [(pos[0] + y, pos[1] + x)
            for y, x in deltas
            if 0 <= pos[1] + x < X and 0 <= pos[0] + y < Y]

def adjacent_occupants(pos: (int, int), grid: [[str]]):
    '''return list of adjacent occupants in reading order'''
    positions = adjacent_positions(pos, grid)
    return [grid[p[0]][p[1]] for p in positions]

def adjacent_units(pos: (int, int), grid: [[str]]):
    '''return list of adjacent units in reading order'''
    occupants = adjacent_occupants(pos, grid)
    return filter(lambda occupant: occupant != '#' and occupant is not None, occupants)

def adjacent_vacant_positions(pos: (int, int), grid: [[str]]):
    '''return list of adjacent vacant positions in reading order'''
    positions = adjacent_positions(pos, grid)
    return [pos for pos in positions if grid[pos[0]][pos[1]] is None]

def reconstruct_path(came_from: {(int, int), (int, int)}, current: (int, int)) -> (int, [(int, int)]):
    path = [current]
    while current in came_from.keys():
        current = came_from[current]
        path.append(current)
    return tuple(reversed(path))

def bfs(start: (int, int), target: (int, int), grid: [[str]]) -> [(int, int)]:
    '''return num steps and path from start to target if reachable else (-1, [])'''
    q = deque()
    q.append(start)
    visited = set()
    visited.add(start)
    came_from = {}
    while len(q) > 0:
        cur = q.popleft()
        if cur == target:
            path = reconstruct_path(came_from, cur)
            return len(path), path
        else:
            for neighbor in adjacent_vacant_positions(cur, grid):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = cur
                    q.append(neighbor)
    return -1, [[]]

class Unit:
    def __init__(self, pos: (int, int), goblin, damage: int = 3):
        self.pos = pos
        self.hp = 200
        self.goblin = goblin
        self.damage = damage
 
    def __str__(self):
        return ('G' if self.goblin else 'E') + ' at ' + str(self.pos) + ' with HP ' + str(self.hp)
 
    def select_target(self, grid: [[str]]):
        '''returns in range opponent with lowest HP in reading order, or None'''
        adjacents = [unit for unit in adjacent_units(self.pos, grid) if unit.goblin != self.goblin]
        if len(adjacents) > 0:
            return min(adjacents, key=lambda unit: unit.hp)
        return None

    def identify_targets_in_range(self, grid: [[str]], targets):
        '''returns list of in range positions'''
        in_range = []
        for target in targets:
            if target != self:
                in_range.extend(adjacent_vacant_positions(target.pos, grid))
        return in_range

    def move(self, grid: [[str]], targets) -> bool:
        '''moves one step towards selected target'''
        if len(adjacent_vacant_positions(self.pos, grid)) == 0:
            return False
        target_positions = self.identify_targets_in_range(grid, targets)
        if len(target_positions) == 0:
            return False
        choices = [(*bfs(self.pos, target_pos, grid), target_pos) for target_pos in target_positions]
        choices = [(distance, path, target) for distance, path, target in choices if distance > 0]
        if len(choices) == 0:
            return False
        sorted_by_distance = sorted(choices, key=lambda pair: pair[0])
        min_distance = sorted_by_distance[0][0]
        fewest_away_choices = list(takewhile(lambda pair: pair[0] == min_distance, sorted_by_distance))
        _, path, _ = min(fewest_away_choices, key=lambda pair: pair[2])
        original_pos = self.pos
        self.pos = path[1]
        grid[original_pos[0]][original_pos[1]] = None
        grid[self.pos[0]][self.pos[1]] = self
        return True

    def attack(self, grid: [[str]], target=None) -> bool:
        '''attack selected target, returning target'''
        if target is None:
            target = self.select_target(grid)
        if target is not None:
            target.hp = max(0, target.hp - self.damage)
        return target

    def take_turn(self, grid: [[str]], targets) -> (bool, bool):
        target = self.select_target(grid)
        if target is not None:
            return False, self.attack(grid, target)
        moved = self.move(grid, targets)
        if moved:
            target = self.attack(grid)
        return moved, target

def parse(lines: [str]) -> ([Unit], [Unit], [[str]]):
    X = len(lines[0].strip())
    Y = len(lines)
    grid = [list(line.strip()) for line in lines]
    goblins = []
    elves = []
    for y in range(Y):
        for x in range(X):
            cell = grid[y][x]
            if cell == '.':
                grid[y][x] = None
            elif cell != '#':
                goblin = cell == 'G'
                unit = Unit((y, x), goblin)
                if goblin:
                    goblins.append(unit)
                else:
                    elves.append(unit)
                grid[y][x] = unit
    return goblins, elves, grid

def print_grid(grid: [[str]]):
    for row in grid:
        for cell in row:
            if cell == '#':
                print('#', end='')
            elif cell is None:
                print(' ', end='')
            else:
                print('G' if cell.goblin else 'E', end='')
        print()

def print_cast(goblins: [Unit], elves: [Unit]):
    for goblin in goblins:
        print(goblin)
    for elf in elves:
        print(elf)

def simulate(goblins: [Unit], elves: [Unit], grid: [[str]], throw=False) -> int:
    round = 0
    while True:
        units = sorted(goblins + elves, key=lambda unit: unit.pos)
        for unit in units:
            if unit.hp > 0:
                _, target = unit.take_turn(grid, elves if unit.goblin else goblins)
                if target is not None and target.hp == 0:
                    if target.goblin:
                        goblins.remove(target)
                    else:
                        if throw:
                            raise ValueError('elf killed in round ' + round)
                        elves.remove(target)
                    grid[target.pos[0]][target.pos[1]] = None
        if len(goblins) == 0 or len(elves) == 0:
            hp = sum(sum(unit.hp for unit in row if unit not in (None, '#')) for row in grid)
            return hp * round
        round += 1

def simulate_with_extra_damage(lines: [str], damage: int):
    goblins, elves, grid = parse(lines)
    for elf in elves:
        elf.damage = damage
    try:
        return simulate(goblins, elves, grid, True)
    except:
        return None

def find_min_attack(lines: [str], lower: int = 4, upper: int = 100) -> int:
    mid = (upper + lower) // 2
    result1 = simulate_with_extra_damage(lines, mid)
    if result1 is None:
        result2 = simulate_with_extra_damage(lines, mid + 1)
        if result2 is not None:
            return result2
        return find_min_attack(lines, mid + 1, upper)
    return find_min_attack(lines, lower, mid)

with open(argv[1]) as fp:
    lines = fp.readlines()
print(simulate(*parse(lines)))
print(find_min_attack(lines))
