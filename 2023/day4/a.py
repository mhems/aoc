from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

def parse_ints(s: str) -> [int]:
    return set(map(int, s.split()))

def count_game(line: str) -> int:
    left, right = line.split('|')
    drawn = parse_ints(right)
    winners = parse_ints(left.split(':')[1])
    return len(winners.intersection(drawn))

def score_game(line: str) -> int:
    left, right = line.split('|')
    drawn = parse_ints(right)
    winners = parse_ints(left.split(':')[1])
    return int(2 ** (count_game(line) - 1))

scores = list(map(score_game, lines))
answer = sum(scores)
print(answer)

qtys = [1] * len(lines)
counts = list(map(count_game, lines))
for i, count in enumerate(counts):
    for j in range(i+1, i + 1 + count):
        qtys[j] += qtys[i]
        
print(sum(qtys))
