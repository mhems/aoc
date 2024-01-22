from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

def remove_garbage(text: str) -> (str, int):
    clean = ''
    i = 0
    total = 0
    while i < len(text):
        if text[i] == '<':
            c = 0
            i += 1
            while text[i] != '>':
                if text[i] == '!':
                    i += 1
                else:
                    c += 1
                i += 1
            i += 1
            total += c
        else:
            clean += text[i]
            i += 1
    return clean.replace(',', ''), total

def score(text: str) -> int:
    total = 0
    cur = 1
    for c in text:
        if c == '{':
            total += cur
            cur += 1
        else:
            cur -= 1
    return total

for line in lines:
    text, amt = remove_garbage(line.strip())
    print(score(text), amt)
