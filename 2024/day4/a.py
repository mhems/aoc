from sys import argv

def num_xmas(wordsearch: [[str]]) -> int:
    def search(delta: (int, int)) -> int:
        target = 'XMAS'
        n = len(target)
        dy, dx = delta
        Y, X = len(wordsearch), len(wordsearch[0])
        count = 0
        for y in range(max(0, -dy * n - 1), min(Y, Y - dy * n + 1)):
            for x in range(max(0, -dx * n - 1), min(X, X - dx * n + 1)):
                word = ''.join(wordsearch[y + i * dy][x + i * dx] for i in range(n))
                count += int(target == word)
        return count
    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return sum(search(delta) for delta in deltas)

def num_mas_x(wordsearch: [[str]]) -> int:
    count = 0
    for y in range(1, len(wordsearch) - 1):
        for x in range(1, len(wordsearch[0]) - 1):
            if wordsearch[y][x] == 'A':
                a = wordsearch[y-1][x-1] + wordsearch[y+1][x+1]
                b = wordsearch[y-1][x+1] + wordsearch[y+1][x-1]
                count += int((a == 'MS' or a == 'SM') and (b == 'MS' or b == 'SM'))
    return count

wordsearch = [list(line.strip()) for line in open(argv[1]).readlines()]
print(num_xmas(wordsearch))
print(num_mas_x(wordsearch))
