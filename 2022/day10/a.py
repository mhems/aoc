from sys import argv

def parse(line: str) -> int:
    tokens = line.split()
    if len(tokens) == 2:
        return int(tokens[1])
    return None

def execute(instructions: [int], cycles_of_interest: {int}, x: int = 1) -> int:
    cycle = 0
    signal_strength = 0
    def tally():
        nonlocal signal_strength
        if cycle in cycles_of_interest:
            signal_strength += x * cycle
    crt = [['.'] * 40 for _ in range(6)]
    def draw():
        if abs(x - (cycle % 40)) <= 1:
            crt[cycle//40][cycle%40] = '#'
    for op in instructions:
        draw()
        if op is None:
            cycle += 1
            tally()
        else:
            cycle += 1
            tally()
            
            draw()
            cycle += 1
            tally()
            x += op
    print('\n'.join(''.join(row) for row in crt))
    return signal_strength

instructions = [parse(line.strip()) for line in open(argv[1]).readlines()]
print(execute(instructions, {20, 60, 100, 140, 180, 220}))
