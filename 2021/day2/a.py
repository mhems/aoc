def part1(cmds: [str]) -> int:
    x, depth = 0, 0
    for cmd in cmds:
        dir, amt = cmd.strip().split()
        amt = int(amt)
        if dir == 'forward':
            x += amt
        elif dir == 'up':
            depth -= amt
        elif dir == 'down':
            depth += amt
    return x * depth

def part2(cmds: [str]) -> int:
    x, depth, aim = 0, 0, 0
    for cmd in cmds:
        dir, amt = cmd.strip().split()
        amt = int(amt)
        if dir == 'forward':
            x += amt
            depth += amt * aim
        elif dir == 'up':
            aim -= amt
        elif dir == 'down':
            aim += amt
    return x * depth

cmds = open('input.txt').readlines()
print(part1(cmds))
print(part2(cmds))
