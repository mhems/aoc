from sys import argv
from collections import Counter

with open(argv[1]) as fp:
    lines = fp.readlines()

columns = [''.join(line[c] for line in lines) for c in range(len(lines[0].strip()))]

def most(s: str) -> str:
    return Counter(s).most_common(1)[0][0]

def least(s: str) -> str:
    return sorted(Counter(s).items(), key=lambda e: e[1])[0][0]
    
print(''.join(most(s) for s in columns))
print(''.join(least(s) for s in columns))
