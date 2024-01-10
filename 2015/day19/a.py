from sys import argv

with open(argv[1]) as fp:
    text = fp.read()

rules, mol = text.strip().split('\n\n')
rules = [tuple(line.strip().split(' => ')) for line in rules.split('\n')]

def apply_rule(rule: (str, str), mol: str) -> {str}:
    results = set()
    i = mol.find(rule[0])
    while i != -1:
        left, right = mol[:i], mol[i+1+len(rule[0])-1:]
        new_mol = left + rule[1] + right
        results.add(new_mol)
        i = mol.find(rule[0], i + 1)
    return results

results = set().union(*[apply_rule(rule, mol) for rule in rules])
print(len(results))