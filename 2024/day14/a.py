from sys import argv
from math import prod
from PIL import Image

def parse(line: str) -> ((int, int), (int, int)):
    def parse_tuple(text: str) -> (int, int):
        return tuple(map(int, text[2:].split(',')))
    p, v = line.strip().split()
    return parse_tuple(p), parse_tuple(v)

def grid_picture(i: int, positions: [(int, int)], width: int, height: int):
    image = Image.new("1", (width, height))
    for pos in positions:
        image.putpixel(pos, 1)
    image.save(f'{i}.png')

def move(input, width: int, height: int, time: int) -> [(int, int)]:
    positions, velocities = [p for p, _ in input], [v for _, v in input]
    i = 0
    while True:
        for p in range(len(positions)):
            positions[p] = ((positions[p][0] + velocities[p][0]) % width,
                            (positions[p][1] + velocities[p][1]) % height)
        if i == time - 1:
            print(safety_factor(positions, width, height))
        if (i - 10) % width == 0 or (i - 64) % height == 0:
            grid_picture(i + 1, positions, width, height)
        if i > 10_000:
            break
        i += 1

def safety_factor(positions: [(int, int)], width: int, height: int) -> int:
    mid_x, mid_y = (width - 1) // 2, (height - 1) // 2
    fs = [0] * 4
    for x, y in positions:
        if x < mid_x and y < mid_y:
            fs[0] += 1
        elif x < mid_x and y > mid_y:
            fs[1] += 1
        elif x > mid_x and y < mid_y:
            fs[2] += 1
        elif x > mid_x and y > mid_y:
            fs[3] += 1
    return prod(fs)

input = [parse(line.strip()) for line in open(argv[1]).readlines()]
if argv[1] == 'example.txt':
    move(input, 11, 7, 100)
else:
    move(input, 101, 103, 100)
