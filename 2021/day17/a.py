from sys import argv

def parse(text: str) -> ((int, int), (int, int)):
    def parse_range(text: str) -> (int, int):
        return tuple(map(int, text[2:].split('..')))
    return tuple(map(parse_range, text[text.index('x'):].split(', ')))

def simulate(velocity: (int, int), x: (int, int), y: (int, int)) -> (bool, int):
    vx, vy = velocity
    startx, endx = x
    starty, endy = y
    x, y, peak = 0, 0, 0
    while True:
        x += vx
        y += vy
        peak = max(peak, y)
        if startx <= x <= endx and starty <= y <= endy:
            return True, peak
        if y < starty:
            return False, peak
        vx = vx - 1 if vx > 0 else vx
        vy -= 1

def find_highest_trajectory(x: (int, int), y: (int, int), n: int = 200) -> (int, int):
    peak = 0
    hitset = set()
    for vx in range(n):
        for vy in range(-n, n):
            hit, height = simulate((vx, vy), x, y)
            if hit:
                peak = max(height, peak)
                hitset.add((vx, vy))
    return peak, len(hitset)

x, y = parse(open(argv[1]).read().strip())
print(find_highest_trajectory(x, y))
