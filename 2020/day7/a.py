from sys import argv

def parse_content(text: str) -> (int, str):
    words = text.strip().split()
    qty = int(words[0]) if words[0] != 'no' else 0
    if words[-1].endswith('s'):
        words[-1] = words[-1].rstrip('s')
    return qty, ' '.join(words[1:])

def parse(line: str) -> (str, [(int, str)]):
    left, right = line.strip('.').split('contain')
    contents = [parse_content(bag) for bag in right.strip().split(', ')]
    return left.strip()[:-1], contents

def num_ancestors(rules: {str: [(int, str)]}, target: str = 'shiny gold bag') -> int:
    def path_exists(src: str) -> bool:
        if src == target:
            return True
        if src == 'other bag':
            return False
        for _, content in rules[src]:
            if path_exists(content):
                return True
        return False
    return sum(int(path_exists(bag)) for bag in rules.keys()) - 1

def num_children(rules: {str: [(int, str)]}, src: str = 'shiny gold bag') -> int:
    def num_bags(bag: str) -> int:
        if bag == 'other bag':
            return 0
        return sum(qty * (1 + num_bags(inner_bag)) for qty, inner_bag in rules[bag])
    return num_bags(src)

rules = dict(parse(line.strip()) for line in open(argv[1]).readlines())
print(num_ancestors(rules))
print(num_children(rules))