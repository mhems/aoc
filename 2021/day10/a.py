from sys import argv
from collections import deque

def score(line: str, part1=True) -> int:
    scores1 = {')': 3, ']': 57, '}': 1197, '>': 25137}
    scores2 = {')': 1, ']': 2, '}': 3, '>': 4}
    expect = {'(': ')', '[': ']', '{': '}', '<': '>'}
    stack = deque()
    for c in line:
        if c in '([{<':
            stack.append(c)
        else:
            if c == expect[stack[-1]]:
                stack.pop()
            elif part1:
                return scores1[c]
            else:
                return 0
    if part1:
        return 0
    score = 0
    while stack:
        score *= 5
        score += scores2[expect[stack.pop()]]
    return score

lines = open(argv[1]).readlines()
print(sum(score(line.strip()) for line in lines))
scores = sorted(filter(None, (score(line.strip(), False) for line in lines)))
print(scores[len(scores)//2])
