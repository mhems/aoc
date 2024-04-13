from sys import argv
from collections import Counter

def insert(polymer: str, rules: {str: str}, n: int) -> int:
    cache = dict()
    def replace(polymer: str) -> str:
        nonlocal cache
        if polymer in cache:
            return cache[polymer]
        out = ''.join(polymer[i] + rules[polymer[i:i+2]]
                    for i in range(len(polymer) - 1)) + polymer[-1]
        cache[polymer] = out
        return out
    def replace_all(polymers: [str], limit: int = 1_000) -> [str]:
        polymers = [replace(polymer) for polymer in polymers]
        for i in range(1, len(polymers)):
            polymers[i] = rules[polymers[i-1][-1] + polymers[i][0]] + polymers[i]
        new_chain = []
        for polymer in polymers:
            if len(polymer) > limit:
                split = len(polymer) // 2
                new_chain.append(polymer[:split])
                new_chain.append(polymer[split:])
            else:
                new_chain.append(polymer)
        return new_chain
    polymers = [polymer]
    for i in range(n):
        polymers = replace_all(polymers)
        print(i, len(polymers))
    counter = Counter(polymers[0])
    for polymer in polymers[1:]:
        counter.update(polymer)
    common = counter.most_common()
    return common[0][1] - common[-1][1]

chunks = open(argv[1]).read().split('\n\n')
polymer = chunks[0].strip()
rules = dict(line.strip().split(' -> ') for line in chunks[1].strip().split('\n'))
print(insert(polymer, rules, 10))
print(insert(polymer, rules, 40))
