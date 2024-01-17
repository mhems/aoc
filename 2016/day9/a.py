from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

def decompress1(s: str) -> int:
    i = 0
    d = 0
    while i < len(s):
        if s[i] == '(':
            xIndex = s.index('x', i)
            span = int(s[i+1: xIndex])
            endIndex = s.index(')', xIndex)
            amt = int(s[xIndex+1:endIndex])
            d += span * amt
            i += (endIndex - i) + 1 + span
        else:
            d += 1
            i += 1
    return d

def decompress2(s: str) -> int:
    i = 0
    d = 0
    while i < len(s):
        if s[i] == '(':
            xIndex = s.index('x', i)
            span = int(s[i+1: xIndex])
            endIndex = s.index(')', xIndex)
            amt = int(s[xIndex+1:endIndex])
            sub = s[endIndex+1: endIndex+1+span]
            d += amt * decompress2(sub)
            i = endIndex + 1 + span
        else:
            d += 1
            i += 1
    return d

for line in lines:
    print(decompress1(line.strip()))
    print(decompress2(line.strip()))
    print()
