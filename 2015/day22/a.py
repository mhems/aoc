from abc import abstractmethod, ABC
from random import choice

class State:
    def __init__(self, hero_hp, hero_mana, hero_armor, mana_spent, boss_hp, boss_damage, effects):
        self.hero_hp = hero_hp
        self.hero_mana = hero_mana
        self.hero_armor = hero_armor
        self.mana_spent = mana_spent
        self.boss_hp = boss_hp
        self.boss_damage = boss_damage
        self.effects = effects
class Effect(ABC):
    def __init__(self, timer: int):
        self.timer = timer
    @abstractmethod
    def apply(self, state: State):
        pass
    @abstractmethod
    def end(self, state: State):
        pass
    def take_turn(self, state: State) -> bool:
        self.apply(state)
        self.timer -= 1
        if self.timer == 0:
            self.end(state)
        return self.timer == 0
class ShieldEffect(Effect):
    def __init__(self):
        super(ShieldEffect, self).__init__(6)
    def apply(self, state: State):
        pass
    def end(self, state: State):
        state.hero_armor = 0
class PoisonEffect(Effect):
    def __init__(self):
        super(PoisonEffect, self).__init__(6)
    def apply(self, state: State):
        state.boss_hp -= 3
    def end(self, state: State):
        pass
class RechargeEffect(Effect):
    def __init__(self):
        super(RechargeEffect, self).__init__(5)
    def apply(self, state: State):
        state.hero_mana += 101
    def end(self, state: State):
        pass

def magic_missile(state: State):
    state.hero_mana -= 53
    state.mana_spent += 53
    state.boss_hp -= 4
def drain(state: State):
    state.hero_mana -= 73
    state.mana_spent += 73
    state.hero_hp += 2
    state.boss_hp -= 2
def shield(state: State):
    state.hero_mana -= 113
    state.mana_spent += 113
    state.hero_armor = 7
    state.effects['shield'] = ShieldEffect()
def poison(state: State):
    state.hero_mana -= 173
    state.mana_spent += 173
    state.effects['poison'] = PoisonEffect()
def recharge(state: State):
    state.hero_mana -= 229
    state.mana_spent += 229
    state.effects['recharge'] = RechargeEffect()

class Game:
    def __init__(self, hero_hp: int, hero_mana: int, boss_hp: int, boss_damage: int, hard: bool = False):
        self.state = State(hero_hp, hero_mana, 0, 0, boss_hp, boss_damage, dict())
        self.hard = hard
    spells = {
        53: magic_missile,
        73: drain,
        113: shield,
        173: poison,
        229: recharge
    }
    def options(self) -> list:
        choices = []
        for cost, func in self.spells.items():
            if self.state.hero_mana >= cost:
                choices.append(func)
        if 'shield' in self.state.effects and shield in choices:
            choices.remove(shield)
        if 'poison' in self.state.effects and poison in choices:
            choices.remove(poison)
        if 'recharge' in self.state.effects and recharge in choices:
            choices.remove(recharge)
        return choices
    def apply_effects(self):
        effects = {}
        for name, effect in self.state.effects.items():
            if not effect.take_turn(self.state):
                effects[name] = effect
        self.state.effects = effects
    def turn(self):
        if self.hard:
            self.state.hero_hp -= 1
            if self.state.hero_hp <= 0:
                return False
        self.apply_effects()
        options = self.options()
        if len(options) == 0:
            return False

        spell = choice(options)
        spell(self.state)
        if self.state.boss_hp <= 0:
            return self.state.mana_spent

        self.apply_effects()
        if self.state.boss_hp <= 0:
            return self.state.mana_spent
        self.state.hero_hp -= max(1, self.state.boss_damage - self.state.hero_armor)
        if self.state.hero_hp <= 0:
            return False

        return self.turn()

with open('input.txt') as fp:
    lines = fp.readlines()
hp, dmg = [int(line.strip().split()[-1]) for line in lines]

def simulate(boss_hp: int, boss_dmg: int, hard: bool = False):
    i = 0
    t = 0
    min = None
    while True:
        game = Game(50, 500, hp, dmg, hard)
        result = game.turn()
        if result is not False:
            if min is None or result < min:
                print(result, t)
                min = result
                i = 0
            else:
                i += 1
                if i > 10000:
                    break
        t += 1
    print(t, 'sims run')

simulate(hp, dmg)
print()
simulate(hp, dmg, True)