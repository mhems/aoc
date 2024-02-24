from sys import argv
from collections import namedtuple as nt
from collections import defaultdict
from math import ceil

Ingredient = nt('Ingredient', ['qty', 'name'])

def parse_ingredient(text: str) -> Ingredient:
    tokens = text.strip().split()
    return Ingredient(int(tokens[0]), tokens[1])

def make_table() -> {Ingredient: (Ingredient)}:
    table = {}
    for line in open(argv[1]).readlines():
        left, right = line.strip().split(' => ')
        ingredients = tuple(parse_ingredient(i) for i in left.strip().split(', '))
        product = parse_ingredient(right.strip())
        if product.name in table:
            raise ValueError(line)
        table[product.name] = product.qty, ingredients
    return table

def merge(d1: {str: int}, d2: {str: int}) -> {str: int}:
    merged = dict(d1)
    for name, amt in d2.items():
        if name not in merged:
            merged[name] = 0
        merged[name] += amt
    return merged

# maps product name to (amount of product produced, amount of ore required)
ore_counts : {str: (int, int)} = {}
surpluses : {str: int} = defaultdict(int)
def count_ore(table: {str: (int, (Ingredient))}, target: Ingredient = None, indent=0) :
    global ore_counts
    if len(ore_counts) == 0:
        for product, (amt, ingredients) in table.items():
            if len(ingredients) == 1 and ingredients[0].name == 'ORE':
                ore_counts[product] = amt, ingredients[0].qty
    if target is None:
        target = Ingredient(1, 'FUEL')
    print(' ' * indent, 'looking to make', target.qty, 'of', target.name)
    target_qty = target.qty
    if surpluses[target.name] > 0:
        print(' ' * indent, 'OOOH and i have', surpluses[target.name], 'already made')
        target_qty = max(0, target_qty - surpluses[target.name])
        surpluses[target.name] = max(0, surpluses[target.name] - target.qty)
        if target_qty == 0:
            return {}
    if target.name in ore_counts:
        return {target.name: target_qty}
    amts = {} # maps product name to amount of product needed to meet target qty
    qty, ingredients = table[target.name]
    need = ceil(target_qty/qty)
    leftover = qty * need - target_qty
    print(' ' * indent, 'will have to make', qty * need, leftover, target.name, 'will be leftover')
    print(' ' * indent, 'these ingredients', ingredients, 'make', qty, 'of', target.name, 'need', need)
    for ingredient in ingredients:
        ore_amts = count_ore(table, Ingredient(ingredient.qty * need, ingredient.name), indent + 2)
        amts = merge(amts, ore_amts)
        print(' ' * indent, ' ', amts)
    if target.name == 'FUEL':
        total = 0
        print('finally', amts)
        for name, amt in amts.items():
            produced, required = ore_counts[name]
            amt_needed = ceil(amt/produced)
            #print(name, produced, required, amt_needed, total)
            total += amt_needed * required
        print('surpluses:', surpluses)
        return total
    print(' ' * indent, 'amts to make', qty * need, 'of', target.name, amts, 'surplus of', leftover)
    surpluses[target.name] += leftover
    return amts

table = make_table()
print(count_ore(table))
