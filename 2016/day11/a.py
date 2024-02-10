from sys import argv
from collections import namedtuple as nt

Component = nt('Component', ['chemical', 'chip'])

def parse_line(line: str) -> [Component]:
    rest = ' '.join(line.strip().split()[4:])[:-1]
    tokens = rest.split(', ')
    if len(tokens) > 1:
        tokens[-1] = tokens[-1][4:]
    def parse_component(text: [str]) -> Component:
        tokens = text.split()
        chip = tokens[-1] == 'microchip'
        chemical = tokens[1].split('-')[0] if chip else tokens[1]
        return Component(chemical, chip)
    return [parse_component(token) for token in tokens]

with open(argv[1]) as fp:
    lines = fp.readlines()

floors = [parse_line(line.strip()) for line in lines[:-1]]
print(floors)