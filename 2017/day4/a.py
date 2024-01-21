from itertools import permutations
from collections import Counter

with open('input.txt') as fp:
    lines = fp.readlines()

def all_unique(elements) -> bool:
    return len(elements) == len(set(elements))

answer = sum(all_unique(line.strip().split()) for line in lines)
print(answer)

def no_anagrams(elements: [str]) -> bool:
    for a, b in permutations(elements, 2):
        if len(a) == len(b):
            if Counter(a) == Counter(b):
                return False
    return True

answer = sum(no_anagrams(line.strip().split()) for line in lines)
print(answer)
