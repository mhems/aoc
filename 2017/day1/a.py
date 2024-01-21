with open('input.txt') as fp:
    text = fp.read().strip()

s = 0
for i in range(0, len(text) - 1):
    if text[i] == text[i+1]:
        s += int(text[i])
    i += 1
if text[-1] == text[0]:
    s += int(text[-1])
print(s)

s = 0
sz = len(text)
half = sz // 2
for i in range(0, len(text)):
    if text[i] == text[(i + half) % sz]:
        s += int(text[i])
    i += 1
print(s)
