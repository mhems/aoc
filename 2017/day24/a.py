from sys import argv
from itertools import groupby

with open(argv[1]) as fp:
    lines = fp.readlines()

def generate_links(components: [(int, int)]) -> {int: [(int, int)]}:
    ports = set()
    for a, b in components:
        ports.add(a)
        ports.add(b)
    links = {}
    for port in ports:
        links[port] = []
        for a, b in components:
            if port == a:
                links[port].append((a, b))
            elif port == b:
                links[port].append((b, a))
    return links

def generate_valid_permutations(target: int,
                                links: {int: [(int, int)]},
                                current: [(int, int)] = None):
    if current is None:
        current = []
    if len(links[target]) > 0:
        for link in links[target]:
            next = list(current)
            next.append(link)
            cloned = {n: list(choices) for n, choices in links.items()}
            cloned[target].remove(link)
            if link[1] != link[0]:
                cloned[link[1]].remove((link[1], link[0]))
            yield from generate_valid_permutations(link[1], cloned, next)
    else:
        yield current

def strongest_bridge_strength(bridges: [[(int, int)]]) -> int:
    return max(sum(sum(step) for step in bridge) for bridge in bridges)

def bridges_of_max_length(bridges: [[(int, int)]]) -> [[(int, int)]]:
    by_length = lambda bridge: len(bridge)
    sorted_by_len = sorted(permutations, key=by_length, reverse=True)
    return next(groupby(sorted_by_len, by_length))[1]

components = [tuple(map(int, line.strip().split('/'))) for line in lines]
permutations = list(generate_valid_permutations(0, generate_links(components)))
print(len(permutations), 'valid maximal bridges')
print('part1', strongest_bridge_strength(permutations))
print('part2', strongest_bridge_strength(bridges_of_max_length(permutations)))
