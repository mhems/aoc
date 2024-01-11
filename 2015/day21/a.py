from collections import namedtuple as nt

Weapon = nt('Weapon', ['name', 'cost', 'damage'])
Armor = nt('Armor', ['name', 'cost', 'armor'])
Ring = nt('Ring', ['name', 'cost', 'damage', 'armor'])
Stats = nt('Stats', ['hp', 'damage', 'armor'])

with open('input.txt') as fp:
    lines = fp.readlines()

def parse_stats(lines: str) -> Stats:
    nums = [int(line.strip().split()[-1]) for line in lines]
    return Stats(*nums)

boss_stats = parse_stats(lines)
my_stats = Stats(100, 0, 0)

def parse_table(tabletext: str) -> [(str, int, int, int)]:
    def parse_row(line: str) -> (str, int, int, int):
        tokens = line.split()
        return (' '.join(tokens[0:-3]), int(tokens[-3]), int(tokens[-2]), int(tokens[-1]))
    return [parse_row(line.strip()) for line in tabletext.split('\n')[1:]]

with open('inventory.txt') as fp:
    text = fp.read()

tables = [parse_table(table) for table in text.strip().split('\n\n')]
weapons = [Weapon(name, cost, damage) for name, cost, damage, _ in tables[0]]
armors = [Armor(name, cost, armor) for name, cost, _, armor in tables[1]]
rings = [Ring(name, cost, damage, armor) for name, cost, damage, armor in tables[2]]
