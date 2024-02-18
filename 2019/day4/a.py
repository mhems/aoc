from sys import argv
from collections import Counter

start = int(argv[1])
stop = int(argv[2])

valid = set()
for n in range(start, stop):
    s = str(n)
    if s[0] == s[1] or s[1] == s[2] or s[2] == s[3] or s[3] == s[4] or s[4] == s[5]:
        digits = [int(digit) for digit in s]
        if all(digits[i] <= digits[i+1] for i in range(5)):
            valid.add(n)
print(len(valid))

count = 0
for n in valid:
    if 2 in Counter(str(n)).values():
        count += 1
print(count)
