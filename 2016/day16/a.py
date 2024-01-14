def next(a: str) -> str:
    b = ''.join(reversed(str(a)))
    b = b.translate({0x30: 0x31, 0x31: 0x30})
    return a + '0' + b

def generate(initial:str, size: int) -> str:
    s = initial
    while len(s) < size:
        s = next(s)
    return s[:size]

def checksum(text: str) -> str:
    def cycle(s: str) -> str:
        pairs = [text[i:i+2] for i in range(0, len(text), 2)]
        return ''.join('1' if pair in ('00',  '11') else '0' for pair in pairs)
    while len(text) % 2 == 0:
        text = cycle(text)
    return text
    
with open('input.txt') as fp:
    initial = fp.read().strip()

print(checksum(generate(initial, 272)))
print(checksum(generate(initial, 35651584)))
