from sys import argv
from functools import reduce

with open(argv[1]) as fp:
    lines = fp.readlines()

def parse_translation(text: str) -> ([str], [str]):
    return tuple(token.strip().split('/') for token in text.strip().split(' => '))

def equals(a: [str], b: [str]) -> bool:
    return all(i == j for i, j in zip(a, b))

def reflect_vertically(pattern: [str]) -> [str]:
    return [''.join(reversed(line)) for line in pattern]

def reflect_horizontally(pattern: [str]) -> [str]:
    return list(reversed(pattern))

def rotate_cw_90(pattern: [str]) -> str:
    return [''.join(line[i] for line in reversed(pattern)) for i in range(len(pattern))]

def make_rules(translations: [([str], [str])]) -> {(str): (str)}:
    rules = {}
    for i, o in translations:
        rules[tuple(i)] = o
        rot90 = rotate_cw_90(i)
        rules[tuple(rot90)] = o
        rot180 = rotate_cw_90(rot90)
        rules[tuple(rot180)] = o
        rot180_vert = reflect_vertically(rot180)
        rules[tuple(rot180_vert)] = o
        rot180_horz = reflect_horizontally(rot180)
        rules[tuple(rot180_horz)] = o
        rot270 = rotate_cw_90(rot180)
        rules[tuple(rot270)] = o
        rot270_vert = reflect_vertically(rot270)
        rules[tuple(rot270_vert)] = o
        rot270_horz = reflect_horizontally(rot270)
        rules[tuple(rot270_horz)] = o
    return rules

def num_on(pattern: [str]) -> int:
    return sum(sum(int(ch == '#') for ch in row) for row in pattern)

def divide(pattern: [str]) -> [[str]]:
    n = len(pattern)
    if n <= 3:
        return [pattern]
    stride = 2 if n % 2 == 0 else 3
    print('  dividing by', stride)
    chunks = []
    rows = [pattern[i:i+stride] for i in range(0, n, stride)]
    print('  ', len(rows), 'rows')
    chunks = []
    print('  ', len(rows[0]), 'lines per row')
    for row in rows:
        for i in range(0, n, stride):
            chunk = []
            for line in row:
                chunk.append(line[i:i+stride])
            chunks.append(chunk)
            print(len(chunks), 'chunks')
    return chunks

def stitch(squares: [[str]]) -> [str]:
    n = len(squares)
    print('stitching', n, 'squares')
    if n == 1:
        return squares[0]
    def small_stitch(squares: [[str]]) -> [str]:
        return [''.join(combo) for combo in zip(*squares)]
    if n == 4:
        return small_stitch(squares[:2]) + small_stitch(squares[2:])
    elif n == 9:
        return small_stitch(squares[:3]) + small_stitch(squares[3:6]) + small_stitch(squares[6:])
    elif n % 2 == 0:
        chunk_size = n // 4
        stitches = [stitch(squares[i-chunk_size:i]) for i in range(chunk_size, n+1, chunk_size)]
        return stitch(stitches)
    else:
        ninth = n // 9
        stitches = [stitch(squares[i-ninth:i]) for i in range(ninth, n+1, ninth)]
        return stitch(stitches)

def iterate(n: int, pattern: [str], rules: {(str): [str]}) -> int:
    for i in range(n):
        d = divide(pattern)
        print('replacing', len(d), 'squares')
        new_squares = [rules[tuple(square)] for square in d]
        pattern = stitch(new_squares)
        print(i, len(pattern), len(new_squares), len(d))
        #print(pattern)
        print('\n'.join(pattern))
        print(num_on(pattern))
        print()
    return num_on(pattern)

n = int(argv[2])
rules = make_rules([parse_translation(line.strip()) for line in lines])
start = ['.#.', '..#', '###']

print(iterate(n, start, rules))

# < 2315618