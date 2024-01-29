from sys import argv

with open(argv[1]) as fp:
    nums = [int(token) for token in fp.read().strip().split()]

class Node:
    def __init__(self, id: int, num_children: int, num_metadata: int):
        self.id = id
        self.metadata = [None] * num_metadata
        self.children = [None] * num_children

def parse_tree(nums: [int], i: int = 0) -> Node:
    node = Node(i, nums.pop(0), nums.pop(0))
    for j in range(len(node.children)):
        node.children[j] = parse_tree(nums, i + j + 1)
    node.metadata = [nums.pop(0) for _ in range(len(node.metadata))]
    return node

def metadata_sum(tree: Node) -> int:
    return sum(tree.metadata) + sum(metadata_sum(child) for child in tree.children)

def value(tree: Node) -> int:
    if len(tree.children) == 0:
        return sum(tree.metadata)
    total = 0
    for metadata in tree.metadata:
        if metadata - 1 < len(tree.children):
            total += value(tree.children[metadata - 1])
    return total

root = parse_tree(nums)
print(metadata_sum(root))
print(value(root))