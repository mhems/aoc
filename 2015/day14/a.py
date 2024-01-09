from sys import argv
from collections import namedtuple as nt

Stats = nt('Stats', ['name', 'speed', 'duration', 'sleep'])

with open(argv[1]) as fp:
    lines = fp.readlines()
duration = int(argv[2])

def parse_stats(line: str) -> Stats:
    tokens = line.strip().split()
    return Stats(tokens[0], int(tokens[3]), int(tokens[6]), int(tokens[13]))

statses = [parse_stats(line) for line in lines]

def run_for(stats: Stats, time: int) -> int:
    duration = stats.duration + stats.sleep
    distance = stats.speed * stats.duration
    num_cycles = time // duration
    remainder = time % duration
    return num_cycles * distance + min(remainder, stats.duration) * stats.speed

print(max(run_for(stats, duration) for stats in statses))

def score(statses: [Stats], time: int) -> int:
    scores = {stats.name : 0 for stats in statses}
    for i in range(1, time+1):
        positions = {stats.name : run_for(stats, i) for stats in statses}
        max_distance = max(positions.values())
        for name, distance in positions.items():
            if distance == max_distance:
                scores[name] += 1
    return max(scores.values())

print(score(statses, duration))
