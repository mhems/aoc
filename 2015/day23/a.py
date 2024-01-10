from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

state = {'a': 0, 'b': 0}
pc = 0

instructions = [line.strip() for line in lines]

def cycle(instruction: str):
    global pc
    tokens = instruction.replace(',', '').split()
    if tokens[0].startswith('j'):
        if tokens[0] == 'jmp':
            pc += int(tokens[1])
        elif tokens[0] == 'jie':
            if state[tokens[1]] % 2 == 0:
                pc += int(tokens[2])
            else:
                pc += 1
        else:
            if state[tokens[1]] == 1:
                pc += int(tokens[2])
            else:
                pc += 1
    else:
        if tokens[0] == 'hlf':
            state[tokens[1]] /= 2
        elif tokens[0] == 'tpl':
            state[tokens[1]] *= 3
        else:
            state[tokens[1]] += 1
        pc += 1
            

while pc < len(instructions):
    cycle(instructions[pc])
print(state)

state = {'a': 1, 'b': 0}
pc = 0

while pc < len(instructions):
    cycle(instructions[pc])
print(state)
