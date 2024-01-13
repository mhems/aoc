from itertools import combinations

with open('input.txt') as fp:
    lines = fp.readlines()

triangles = [tuple(map(int, line.strip().split())) for line in lines]

def is_triangle(triangle: (int, int, int)) -> bool:
    return sum(triangle[0:2]) > triangle[2] and sum(triangle[1:]) > triangle[0] and triangle[0] + triangle[2] > triangle[1]

def num_valid(triangles: [(int, int, int)]) -> int:
    return sum(int(is_triangle(triangle)) for triangle in triangles)

print(num_valid(triangles))

triangles = []
for i in range(0, len(lines), 3):
    triangles.extend(tuple(map(int, (lines[i+d].strip().split()[c] for d in range(3)))) for c in range(3))

print(num_valid(triangles))
