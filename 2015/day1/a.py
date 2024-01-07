from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()
line = lines[0]
print(sum(1 if ch == '(' else -1 for ch in line.strip()))

c = 0
for i, ch in enumerate(line):
    c += 1 if ch == '(' else -1
    if c < 0:
        print(i+1)
        break
