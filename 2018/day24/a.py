from sys import argv

class Group:
    def __init__(self, line: str, i: int):
        self.i = i
        if line is None:
            return
        tokens = line.strip().split()
        self.size = int(tokens[0])
        self.hp = int(tokens[4])
        self.initiative = int(tokens[-1])
        damage_index = tokens.index('damage')
        self.damage = int(tokens[damage_index - 2])
        self.type = tokens[damage_index - 1]
        self.weaknesses = []
        self.immunities = []
        if '(' in line:
            traits = line[line.index('(') + 1: line.index(')')].split(';')
            for trait in traits:
                tokens = trait.split()
                if tokens[0] == 'weak':
                    self.weaknesses = [t.strip(',') for t in tokens[2:]]
                elif tokens[0] == 'immune':
                    self.immunities = [t.strip(',') for t in tokens[2:]]
    def copy(self):
        clone = Group(None, self.i)
        clone.size = self.size
        clone.hp = self.hp
        clone.initiative = self.initiative
        clone.damage = self.damage
        clone.type = self.type
        clone.weaknesses = self.weaknesses
        clone.immunities = self.immunities
        return clone
    
    @property
    def effective_power(self):
        return self.size * self.damage

    def damage_to(self, target):
        damage = 0
        if self.type not in target.immunities:
            damage = self.effective_power
            if self.type in target.weaknesses:
                damage *= 2
        return damage

    def attack(self, target):
        units_gone = min(target.size, self.damage_to(target) // target.hp)
        target.size -= units_gone
        #print('Group %d removes %d units from Group %d (%d remain)' %
        #      (self.i, units_gone, target.i, target.size))

    def select(self, targets):
        if len(targets) == 0:
            return None
        top_choice = sorted(targets,
               key=lambda g: (self.damage_to(g), g.effective_power, g.initiative),
               reverse=True)[0]
        if self.damage_to(top_choice) == 0:
            return None
        return top_choice

def select(immune: [Group], infection: [Group]) -> {Group: Group}:
    attack_map = {}
    all_groups = sorted(immune + infection,
                        key=lambda group: (group.effective_power, group.initiative),
                        reverse=True)
    immune_choices = set(immune)
    infection_choices = set(infection)
    for group in all_groups:
        is_immune = group in immune
        choices = infection_choices if is_immune else immune_choices
        selection = group.select(choices)
        if selection is not None:
            choices.remove(selection)
            attack_map[group] = selection
            #system = 'Immune' if is_immune else 'Infection'
            #print('%s Group %d selects Group %d for %d damage' %
            #      (system, group.i, selection.i, group.damage_to(selection)))
    return attack_map

def attack(immune: [Group], infection: [Group], attack_map: {Group: Group}):
    all_groups = sorted(immune + infection, key=lambda group: group.initiative, reverse=True)
    for group in all_groups:
        if group.size > 0 and group in attack_map:
            defendant = attack_map[group]
            group.attack(defendant)
            if defendant.size <= 0:
                #print('  removing Group %d' % defendant.i)
                if defendant in immune:
                    immune.remove(defendant)
                else:
                    infection.remove(defendant)

def clone(army: [Group]) -> [Group]:
    return [group.copy() for group in army]

def battle(immune: [Group], infection: [Group], boost: int = 0) -> int:
    immune = clone(immune)
    infection = clone(infection)
    for group in immune:
        group.damage += boost
    while True:
        #print('Immune System')
        #for group in immune:
        #    print('  Group %d: %d units' % (group.i, group.size))
        #print('Infection System')
        #for group in infection:
        #    print('  Group %d: %d units' % (group.i, group.size))
        previous_immune_remaining = sum(g.size for g in immune)
        previous_infection_remaining = sum(g.size for g in infection)
        attack_map = select(immune, infection)
        attack(immune, infection, attack_map)
        immune_remaining = sum(g.size for g in immune)
        infection_remaining = sum(g.size for g in infection)
        if previous_immune_remaining == immune_remaining and previous_infection_remaining == infection_remaining:
            return 0
        if immune_remaining == 0:
            return -infection_remaining
        if infection_remaining == 0:
            return immune_remaining
        #print('-' * 20)

def find_min_boost(immune: [Group], infection: [Group], lo: int = 0, hi: int = 1_000_000) -> int:
    mid = (hi + lo) // 2
    result = battle(immune, infection, mid)
    if result == 0:
        return battle(immune, infection, mid + 1)
    if result < 0:
        return find_min_boost(immune, infection, mid, hi)
    return find_min_boost(immune, infection, lo, mid)

with open(argv[1]) as fp:
    text = fp.read()

first, second = text.split('\n\n')
immune = [Group(line.strip(), i+1) for i, line in enumerate(first.strip().split('\n')[1:])]
infection = [Group(line.strip(), i+1) for i, line in enumerate(second.strip().split('\n')[1:])]
print(battle(immune, infection))
print(find_min_boost(immune, infection))
