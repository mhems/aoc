from collections import namedtuple as nt

Ingredient = nt('Ingredient', ['name', 'capacity', 'durability', 'flavor', 'texture', 'calories'])

with open('input.txt') as fp:
    lines = fp.readlines()
total = 100
calorie_count = 500

def parse_ingredient(line: str) -> Ingredient:
    tokens = line.strip().split()
    return Ingredient(tokens[0].rstrip(':'),
                      int(tokens[2].rstrip(',')),
                      int(tokens[4].rstrip(',')),
                      int(tokens[6].rstrip(',')),
                      int(tokens[8].rstrip(',')),
                      int(tokens[10]))

ingredients = [parse_ingredient(line.strip()) for line in lines]

def score(recipe: {Ingredient: int}, calorie_count) -> int:
    if calorie_count is not None:
        calories = sum(amt * ingredient.calories for ingredient, amt in recipe.items())
        if calories != calorie_count:
            return 0
    capacity = max(0, sum(amt * ingredient.capacity for ingredient, amt in recipe.items()))
    durability = max(0, sum(amt * ingredient.durability for ingredient, amt in recipe.items()))
    flavor = max(0, sum(amt * ingredient.flavor for ingredient, amt in recipe.items()))
    texture = max(0, sum(amt * ingredient.texture for ingredient, amt in recipe.items()))
    return capacity * durability * flavor * texture

def generate_recipes(total: int, calorie_count= None):
    for i in range(total+1):
        for j in range(total+1):
            for k in range(total+1):
                for l in range(total+1):
                    if i + j + k + l == total:
                        recipe = {ingredients[0]:i, ingredients[1]:j, ingredients[2]:k, ingredients[3]:l}
                        n = score(recipe, calorie_count)
                        if n > 0:
                            yield n
                            
print(max(generate_recipes(total)))

print(max(generate_recipes(total, calorie_count)))
