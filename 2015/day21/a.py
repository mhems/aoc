from collections import namedtuple as nt
from itertools import chain, combinations

Weapon = nt('Weapon', ['name', 'cost', 'damage'])
Armor = nt('Armor', ['name', 'cost', 'armor'])
Ring = nt('Ring', ['name', 'cost', 'damage', 'armor'])
Stats = nt('Stats', ['hp', 'damage', 'armor'])

with open('input.txt') as fp:
    lines = fp.readlines()

def parse_stats(lines: str) -> Stats:
    nums = [int(line.strip().split()[-1]) for line in lines]
    return Stats(*nums)

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

# for hero to win, below inequality must be True:
#   enemy.hp*enemy.dmg + hero.hp*enemy.armor <= hero.hp*hero.dmg + enemy.hp*hero.armor
def make_win_function(boss_stats: Stats, hero_hp: int):
    def wins(hero_damage: int, hero_armor: int):
        lhs = boss_stats.hp*boss_stats.damage + hero_hp*boss_stats.armor
        rhs = hero_hp*hero_damage + boss_stats.hp*hero_armor
        return lhs <= rhs
    return wins

boss_stats = parse_stats(lines)
win_func = make_win_function(boss_stats, 100)

def generate_choices():
    for weapon in weapons:
        for armor in armors + [Armor('none', 0, 0)]:
            for ringset in chain.from_iterable(combinations(rings, r) for r in range(2+1)):
                spent = sum(ring.cost for ring in ringset) + weapon.cost + armor.cost
                damage = sum(ring.damage for ring in ringset) + weapon.damage
                defense = sum(ring.armor for ring in ringset) + armor.armor
                yield (spent, damage, defense)

def generate_min_winning_purchases():
    cur_min = 2**16
    for cost, damage, defense in generate_choices():
        if win_func(damage, defense) and cost < cur_min:
            cur_min = cost
    return cur_min

def generate_max_losing_purchases():
    cur_max = 0
    for cost, damage, defense in generate_choices():
        if not win_func(damage, defense) and cost > cur_max:
            cur_max = cost
    return cur_max

print(generate_min_winning_purchases())
print(generate_max_losing_purchases())
