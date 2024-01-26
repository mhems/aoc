from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

def up(lines: [str], row: int, col: int) -> (str, int):
    row -= 1
    next = lines[row][col]
    s = ''
    while next != '+' and next != ' ':
        if next.isalpha():
            s += next
        row -= 1
        next = lines[row][col]
    return s, row

def down(lines: [str], row: int, col: int) -> (str, int):
    row += 1
    next = lines[row][col]
    s = ''
    while next != '+' and next != ' ':
        if next.isalpha():
            s += next
        row += 1
        next = lines[row][col]
    return s, row

def left(lines: [str], row: int, col: int) -> (str, int):
    col -= 1
    next = lines[row][col]
    s = ''
    while next != '+' and next != ' ':
        if next.isalpha():
            s += next
        col -= 1
        next = lines[row][col]
    return s, col

def right(lines: [str], row: int, col: int) -> (str, int):
    col += 1
    next = lines[row][col]
    s = ''
    while next != '+' and next != ' ':
        if next.isalpha():
            s += next
        col += 1
        next = lines[row][col]
    return s, col

def walk(lines: [str]) -> str:
    col = lines[0].index('|')
    s, row = down(lines, 0, col)
    visited = s
    vert = True
    steps = row
    while lines[row][col] == '+':
        if vert:
            start_col = col
            if lines[row][col-1] == ' ':
                s, col = right(lines, row, col)
            elif lines[row][col+1] == ' ':
                s, col = left(lines, row, col)
            steps += abs(start_col - col)
            vert = False
        else:
            start_row = row
            if lines[row-1][col] == ' ':
                s, row = down(lines, row, col)
            elif row == len(lines) - 1 or lines[row+1][col] == ' ':
                s, row = up(lines, row, col)
            steps += abs(start_row - row)
            vert = True
        visited += s
    return visited, steps

print(walk(lines))