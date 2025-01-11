from sys import argv
from collections import namedtuple as nt
from functools import cache
from heapq import heappush, heappop
from math import prod

ORE, CLAY, OBSIDIAN, GEODE = range(4)
Blueprint = nt('Blueprint', ['id',
                             'ore_robot_cost_in_ore', 'clay_robot_cost_in_ore',
                             'obsidian_robot_cost_in_ore', 'obsidian_robot_cost_in_clay',
                             'geode_robot_cost_in_ore', 'geode_robot_cost_in_obsidian'])

def parse(i: int, line: str) -> Blueprint:
    tokens = line.strip().split()
    return Blueprint(i, *tuple(int(tokens[i]) for i in (6, 12, 18, 21, 27, 30)))

@cache
def triangle(n: int) -> int:
    return (n * (n-1)) // 2

@cache
def best_case(time_left: int, robots: (int), ores: (int)) -> int:
    return ores[GEODE] + robots[GEODE] * time_left + triangle(time_left)

def max_geodes(blueprint: Blueprint, time: int) -> int:
    q = []
    heappush(q, (0, time, (1, 0, 0, 0), (0, 0, 0, 0)))
    considered = 0  
    max_ore_need = max(blueprint.ore_robot_cost_in_ore, blueprint.clay_robot_cost_in_ore, blueprint.obsidian_robot_cost_in_ore, blueprint.geode_robot_cost_in_ore)
    
    @cache
    def heuristic(time_left: int, robots: (int), qtys: (int)) -> int:
        return (
            -100000000000000000000000000 * int(time_left < 2) + 
            -100 * time_left + 
            
            -100000000000 * robots[GEODE] +
            -1000000000 * robots[OBSIDIAN] +
            -10000000 * robots[CLAY] +
            -100000 * robots[ORE] +
            
            10000000 * int(qtys[OBSIDIAN] > blueprint.geode_robot_cost_in_obsidian) +
            100 * int(qtys[CLAY] > blueprint.obsidian_robot_cost_in_clay)
        )
    
    @cache
    def make_state(time_left: int, robots: (int), robot_deltas: (int), qtys: (int)) -> (int):
        return (time_left - 1,
                tuple(map(sum, zip(robots, robot_deltas))),
                (qtys[ORE] - blueprint.geode_robot_cost_in_ore * robot_deltas[GEODE]
                           - blueprint.obsidian_robot_cost_in_ore * robot_deltas[OBSIDIAN]
                           - blueprint.clay_robot_cost_in_ore * robot_deltas[CLAY]
                           - blueprint.ore_robot_cost_in_ore * robot_deltas[ORE]
                           + robots[ORE],
                 qtys[CLAY] - blueprint.obsidian_robot_cost_in_clay * robot_deltas[OBSIDIAN]
                            + robots[CLAY],
                 qtys[OBSIDIAN] - blueprint.geode_robot_cost_in_obsidian * robot_deltas[GEODE]
                                + robots[OBSIDIAN],
                 qtys[GEODE] + robots[GEODE]))

    def enqueue(time_left: int, robots: (int), robot_deltas: (int), qtys: (int)):
        state = make_state(time_left, robots, robot_deltas, qtys)
        heappush(q, (heuristic(*state), ) + state)
    
    best = 0
    skipped = 0
    itr = None

    while q:
        _, time_left, robots, ores = heappop(q)
        if best_case(time_left, robots, ores) <= best:
            skipped += 1
            continue
        considered += 1
        if considered >= 30_000_000:
            break
        if time_left == 0:
            if ores[GEODE] > best:
                best = ores[GEODE]
                itr = considered - 1
                print('*' * 50, best, ores[GEODE], itr, len(q), flush=True)
            continue
        if time_left > 1 and ores[ORE] >= blueprint.geode_robot_cost_in_ore and ores[OBSIDIAN] >= blueprint.geode_robot_cost_in_obsidian:
            enqueue(time_left, robots, (0, 0, 0, 1), ores)
        elif time_left > 1 and ores[ORE] >= blueprint.obsidian_robot_cost_in_ore and ores[CLAY] >= blueprint.obsidian_robot_cost_in_clay and robots[OBSIDIAN] < blueprint.geode_robot_cost_in_obsidian:
            enqueue(time_left, robots, (0, 0, 1, 0), ores)
        elif time_left > 1 and ores[ORE] >= blueprint.clay_robot_cost_in_ore and robots[CLAY] < blueprint.obsidian_robot_cost_in_clay:
            enqueue(time_left, robots, (0, 1, 0, 0), ores)
        if time_left > 1 and ores[ORE] >= blueprint.ore_robot_cost_in_ore and robots[ORE] < max_ore_need:
            enqueue(time_left, robots, (1, 0, 0, 0), ores)
        enqueue(time_left, robots, (0, 0, 0, 0), ores)
    print(itr, considered, best, skipped, flush=True)
    print()
    return best

blueprints = [parse(i + 1, line.strip()) for i, line in enumerate(open(argv[1]).readlines())]
print(sum(blueprint.id * max_geodes(blueprint, 24) for blueprint in blueprints))
print(prod(max_geodes(blueprint, 32) for blueprint in blueprints[:3]))
