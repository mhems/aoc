from sys import argv

def rotate(elements: [int], n: int) -> [int]:
    if n > 0:
        return elements[n:] + elements[:n]
    elif n < 0:
        return elements[:n] + elements[-n:]
    return elements

def play(labels: [int], n: int = 100) -> int:
    pos = 0
    N = len(labels)
    for _ in range(n):
        cur = labels[pos]
        picked = labels[(pos + 1): min(pos + 1 + 3, N)]
        if len(picked) < 3:
            picked += labels[0: 3 - len(picked)]
        for p in picked:
            labels.remove(p)
        dest = cur - 1
        if dest == 0:
            dest = 9
        while dest in picked:
            dest -= 1
            if dest == 0:
                dest = 9
        index = labels.index(dest)
        for i, e in enumerate(picked):
            labels.insert(index + i + 1, e)
        labels = rotate(labels, labels.index(cur) - pos)
        pos = (pos + 1) % N
    index = labels.index(1)
    return ''.join(map(str, labels[index+1:] + labels[:index]))

labeling = [int(n) for n in argv[1]]
print(play(labeling))