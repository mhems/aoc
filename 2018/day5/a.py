from sys import argv
from tqdm import tqdm

with open(argv[1]) as fp:
    text = fp.read().strip()

def scan(s: str) -> int:
    while True:
        for i in range(len(s) - 1):
            if s[i] != s[i+1] and s[i].lower() == s[i+1].lower():
                break
        else:
            break
        s = s[:i] + s[i+2:]
    return len(s)

print(scan(text))

def fully_react(s: str) -> int:
    min_ = len(s)
    for ch in tqdm(range(ord('a'), ord('z') + 1)):
        cand = s.replace(chr(ch), '')
        cand = cand.replace(chr(ch).upper(), '')
        units = scan(cand)
        if units < min_:
            min_ = units
    return min_

print(fully_react(text))
