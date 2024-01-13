from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

def follow1(initial: int, path: str) -> str:
    pos = initial
    for dir in path:
        if dir == 'U':
            if pos > 3:
                pos -= 3
        elif dir == 'D':
            if pos < 7:
                pos += 3
        elif dir == 'L':
            if pos % 3 != 1:
                pos -= 1
        elif dir == 'R':
            if pos % 3 != 0:
                pos += 1
    return pos

def follow2(initial, path: str) -> str:
    pos = str(initial)
    for dir in path:
        if dir == 'U':
            if pos in '678':
                pos = '234'['678'.index(pos)]
            elif pos in 'ABC':
                pos = '678'['ABC'.index(pos)]
            elif pos == 'D':
                pos = 'B'
            elif pos == '3':
                pos = '1'
        elif dir == 'D':
            if pos in '234':
                pos = '678'['234'.index(pos)]
            elif pos in '678':
                pos = 'ABC'['678'.index(pos)]
            elif pos == '1':
                pos = '3'
            elif pos == 'B':
                pos = 'D'
        elif dir == 'L':
            if pos in '48C':
                pos = '37B'['48C'.index(pos)]
            elif pos in '37B':
                pos = '26A'['37B'.index(pos)]
            elif pos == '9':
                pos = '8'
            elif pos == '6':
                pos = '5'
        else:
            if pos in '26A':
                pos = '37B'['26A'.index(pos)]
            elif pos in '37B':
                pos = '48C'['37B'.index(pos)]
            elif pos == '5':
                pos = '6'
            elif pos == '8':
                pos = '9'
    return pos

def get_code(paths: [str], follow) -> int:
    code = []
    pos = 5
    for line in lines:
        pos = follow(pos, line.strip())
        code.append(pos)
    return ''.join(map(str, code))

print(get_code(lines, follow1))
print(get_code(lines, follow2))