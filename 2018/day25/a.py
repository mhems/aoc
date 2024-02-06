from sys import argv
from itertools import permutations

with open(argv[1]) as fp:
    lines = fp.readlines()

def distance(v1: [int], v2: [int]) -> int:
    return sum(abs(a - b) for a, b in zip(v1, v2))

def remove_unreachable(positions: {(int, int, int, int)}) -> {(int, int, int, int)}:
    s = set()
    for position in positions:
        min_dist = 1e6
        for pos2 in positions:
            if position != pos2:
                d = distance(position, pos2)
                if d < min_dist:
                    min_dist = d
        if min_dist > 3:
            s.add(tuple(position))
    for p in s:
        positions.remove(p)
    return s

def group(positions: {(int, int, int, int)}) -> [[(int, int, int, int)]]:
    distances = {(v1, v2): distance(v1, v2) for v1, v2 in permutations(positions, 2)}
    constellations = []
    for star in positions:
        merged = False
        new_constellations = []
        constellation_with_star = None
        for constellation in constellations:
            in_this_one = False
            for other_star in constellation:
                if star != other_star:
                    t = (star, other_star) if other_star > star else (other_star, star)
                    if distances[t] <= 3:
                        merged = True
                        in_this_one = True
                        break
            if in_this_one:
                if constellation_with_star is None:
                    constellation_with_star = constellation + [star]
                else:
                    constellation_with_star.extend(constellation)
            else:
                new_constellations.append(constellation)
        if constellation_with_star is not None:
            new_constellations.append(constellation_with_star)
        if not merged:
            new_constellations.append([star])
        constellations = new_constellations
    return constellations

positions = set(tuple(map(int, line.strip().split(','))) for line in lines)
print(len(positions), 'starting')
alone = remove_unreachable(positions)
print(len(alone), 'alone')
print(len(positions), 'remaining')
constellations = group(positions)
print(len(constellations), '+', len(alone), '=', len(constellations) + len(alone))
