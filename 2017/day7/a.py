from sys import argv
from collections import namedtuple as nt
from collections import Counter

Node = nt('Node', ['name', 'weight', 'parent', 'children'])

def parse_node(line: str) -> Node:
    tokens = line.strip().split()
    name = tokens[0]
    weight = int(tokens[1][1:-1])
    children = ''.join(tokens[3:]).split(',') if len(tokens) > 2 else []
    return Node(name, weight, [], children)

def parse_nodes(lines: [str]) -> {str: Node}:
    nodes = {}
    for line in lines:
        node = parse_node(line.strip())
        nodes[node.name] = node
    for _, node in nodes.items():
        children = [nodes[name] for name in node.children]
        node.children.clear()
        node.children.extend(children)
    for _, node in nodes.items():
        for child in node.children:
            child.parent.append(node)
    return nodes

def get_parent(node: Node) -> Node:
    while len(node.parent) > 0:
        node = node.parent[0]
    return node

with open(argv[1]) as fp:
    lines = fp.readlines()
nodes = parse_nodes(lines)

root = None
for name, node in nodes.items():
    root = get_parent(node)
    print('parent of', name, 'is', root.name)
    break

def find_weight(root: Node) -> int:
    if len(root.children) == 0:
        return root.weight
    weights = [find_weight(child) for child in root.children]
    freqs = Counter(weights)
    if len(freqs) == 2:
        expected, oddball = freqs.most_common()
        i = weights.index(oddball[0])
        print(root.children[i].name, root.children[i].weight - (oddball[0] - expected[0]))
    return sum(weights) + root.weight

find_weight(root)
