from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

def build_graph(lines: [str]) -> {int: [int]}:
    node_map = {}
    for line in lines:
        tokens = line.strip().split(' <-> ')
        node_map[int(tokens[0])] = [int(e) for e in tokens[1].split(', ')]
    return node_map

def get_reachable(graph: {int: [int]}, start: int, reachable: {int}):
    reachable.add(start)
    for node in graph[start]:
        if node not in reachable:
            reachable.add(node)
            get_reachable(graph, node, reachable)

def num_groups(graph: {int: [int]}) -> int:
    nodes = set(graph.keys())
    num = 0
    while len(nodes) > 0:
        num += 1
        node = nodes.pop()
        reachable = set()
        get_reachable(graph, node, reachable)
        nodes -= reachable
    return num

graph = build_graph(lines)
reachable = set()
get_reachable(graph, 0, reachable)
print(len(reachable))
print(num_groups(graph))
