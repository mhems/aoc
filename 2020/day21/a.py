from sys import argv
from functools import reduce

def parse() -> [({str}, {str})]:
    ingredients = []
    for line in open(argv[1]).readlines():
        left, right = line.strip().rstrip(')').split('(contains')
        left = set(left.strip().split())
        right = set(right.strip().split(', '))
        ingredients.append((left, right))
    return ingredients

def collate(ingredient_list: [{str}, {str}]) -> ({str: {str}}, {str}):
    d = dict()
    all_ingredients = set()
    for ingredients, allergens in ingredient_list:
        all_ingredients.update(set(ingredients))
        for allergen in allergens:
            if allergen not in d:
                d[allergen] = set(ingredients)
            else:
                d[allergen].intersection_update(set(ingredients))
    candidates = reduce(lambda s1, s2: set(s1).union(set(s2)), d.values())
    return d, all_ingredients - candidates

def deduce(candidates: {str: {str}}) -> str:
    fixed = set()
    def fix(allergen: str, ingredients: {str}):
        if len(ingredients) == 1:
            found = next(iter(ingredients))
            fixed.add(found)
            for other, v in candidates.items():
                if other != allergen and found in v:
                    v.remove(found)
                    if len(v) == 1:
                        fix(other, v)
    while any(len(v) > 1 for v in candidates.values()):
        for allergen, ingredients in candidates.items():
            if allergen not in fixed:
                if len(ingredients) == 1:
                    fix(allergen, ingredients)
    return ','.join(next(iter(candidates[key])) for key in sorted(candidates.keys()))

ingredients_list = parse()
collated, inert = collate(ingredients_list)
print(sum(len(ingredients.intersection(inert)) for ingredients, _ in ingredients_list))
print(deduce(collated))
