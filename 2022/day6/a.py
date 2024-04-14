def packet_start(text: str, n: int) -> int:
    before = text[:n-1]
    for i, l in enumerate(text[n-1:]):
        if len(set((l, *before))) == n:
            return i + n
        before = text[i+1:i+n]
    return -1

text = open('input.txt').read().strip()
print(packet_start(text, 4))
print(packet_start(text, 14))