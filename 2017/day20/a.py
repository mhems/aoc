with open('input.txt') as fp:
    lines = fp.readlines()

def parse(line: str) -> ((int, int, int), (int, int, int), (int, int, int)):
    def parse_triple(text: str) -> (int, int, int):
        return tuple(map(int, text[3:-1].split(',')))
    tokens = line.strip().split(', ')
    return parse_triple(tokens[0]), parse_triple(tokens[1]), parse_triple(tokens[2])

def magnitude(vector: (int, int, int)) -> int:
    return sum(a * a for a in vector)

stats = [(i, parse(line.strip())) for i, line in enumerate(lines)]
stats.sort(key = lambda tt: (magnitude(tt[1][2]), magnitude(tt[1][1]), magnitude(tt[1][0])))

print(stats[0][0])
