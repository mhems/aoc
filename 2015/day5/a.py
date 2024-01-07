from sys import argv
from collections import Counter
from itertools import pairwise
import re

with open(argv[1]) as fp:
    lines = fp.readlines()

def is_nice(s: str) -> bool:
    counts = Counter(s)
    num_vowels = sum(counts[vowel] for vowel in 'aeiou')
    num_adj = sum(int(a == b) for a, b in pairwise(s))
    ok = all(sub not in s for sub in ('ab', 'cd', 'pq', 'xy'))
    return num_vowels >= 3 and num_adj > 0 and ok

regex1 = re.compile(r'(.).\1')
regex2 = re.compile(r'(..).*\1')
def is_nice2(s: str) -> bool:
    return (re.search(regex1, s) is not None and
        re.search(regex2, s) is not None)

print(sum(int(is_nice(s.strip())) for s in lines))
print(sum(int(is_nice2(s.strip())) for s in lines))
