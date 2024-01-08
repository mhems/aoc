from sys import argv
from functools import reduce
import operator

with open(argv[1]) as fp:
    lines = fp.readlines()

def count(s: str) -> (int, int):
    data = 0
    i = 1
    while i < len(s) - 1:
        if s[i] == '\\':
            if s[i+1] == 'x':
                i += 4
            else:
                i += 2
        else:
            i += 1
        data += 1
    return len(s), data

def count_encoded(s: str) -> (int, int):
    new_s = s.replace("\\", "\\\\")
    new_s = new_s.replace("\"", "\\\"")
    return len(new_s) + 2, count(s)[0]

def compute_answer(func) -> int:
    answer = reduce(lambda x, y: tuple(map(operator.add, x, y)),
                (func(line.strip()) for line in lines),
                (0, 0))
    return answer[0] - answer[1]

print(compute_answer(count))
print(compute_answer(count_encoded))
