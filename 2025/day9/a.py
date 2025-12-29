import sys
from itertools import combinations, product
from collections import defaultdict

coords = [tuple(map(int, line.rstrip().split(','))) for line in open(sys.argv[1]).readlines()]
N = len(coords)
combos = list(combinations(coords, 2))

def get_extrema(points):
    xmin = min(x for x, _ in points)
    xmax = max(x for x, _ in points)
    ymin = min(y for _, y in points)
    ymax = max(y for _, y in points)
    return xmin, xmax, ymin, ymax

xmin, xmax, ymin, ymax = get_extrema(coords)

def build_edges(coords, width):
    ys = list()
    edges = set(coords)
    for i in range(1, N + 1):
        (xp, yp), (xn, yn) = coords[i-1], coords[i % N]
        xmin, xmax, ymin, ymax = get_extrema(((xp, yp), (xn, yn)))
        if yp == yn:
            if width > 100 and abs(xp - xn) > width//2:
                ys.append(yp)
            for x in range(xmin, xmax):
                edges.add((x, yp))
        else:
            for y in range(ymin, ymax):
                edges.add((xp, y))
    ex_min_y, ex_max_y = sorted(ys) if ys else (0, 0)
    return edges, ex_min_y, ex_max_y

edges, ex_min_y, ex_max_y = build_edges(coords, xmax-xmin)

def build_scanlines():
    scanlines = defaultdict(list)
    for i in range(1, N + 1):
        (xp, yp), (xn, yn) = coords[i-1], coords[i % N]
        if xp == xn:
            for y in range(min(yp, yn), max(yp, yn)):
                scanlines[y].append(xp)
        else:
            assert yp == yn
    for scanline in scanlines.values():
        scanline.sort()
    return scanlines

scanlines = build_scanlines()

def in_polygon(pos):
    if pos in edges:
        return True
    return sum(1 for px in scanlines.get(pos[1], []) if px > pos[0]) % 2 == 1

def main():
    max_area = 0
    max_internal_area = 0
    for a, b in combos:
        xmin, xmax, ymin, ymax = get_extrema((a, b))
        area = abs(xmax - xmin + 1) * abs(ymax - ymin + 1)
        if area > max_area:
            max_area = area
        corners = set(product([xmin, xmax], [ymin, ymax]))
        if len(corners) == 4 and area > max_internal_area:
            corners.difference_update(a, b)
            if all(in_polygon(p) for p in corners) and (ymin >= ex_max_y or ymax <= ex_min_y):
                max_internal_area = area
    return max_area, max_internal_area

print('\n'.join(map(str, main())))

def save_to_svg():
    path = "M " + " L ".join(f"{x} {y}" for x, y in coords) + " Z"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
        viewBox="{xmin} {ymin} {xmax - xmin} {ymax - ymin}">
        <path d="{path}" fill="fill"/>
    </svg>"""

    with open(sys.argv[1].split('.')[0] + '.svg', "w") as f:
        f.write(svg)

save_to_svg()