from sys import argv

def seat(encoding: str) -> int:
    def decode(text: str, low_ch: str, high_ch: str) -> int:
        return int(text.replace(low_ch, '0').replace(high_ch, '1'), 2)
    row = decode(encoding[:7], 'F', 'B')
    col = decode(encoding[7:], 'L', 'R')
    return row * 8 + col

encodings = [line.strip() for line in open(argv[1]).readlines()]
ordered = sorted(seat(encoding) for encoding in encodings)
print(ordered[-1])
for i in range(len(ordered) - 2):
    a, b = ordered[i: i+2]
    if a + 1 != b:
        print(a + 1)
        break
