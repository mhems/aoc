from collections import deque

def make_stacks(lines: [str]) -> [deque]:
    indices = [i for i, ch in enumerate(lines[-1]) if ch != ' ']
    deques = [deque() for _ in range(len(indices))]
    for i, index in enumerate(indices):
        for line in lines[:-1]:
            if line[index] != ' ':
                deques[i].appendleft(line[index])
    return deques

def rearrange(stacks: [deque], moves: (int, int, int), multiple: bool = False) -> str:
    for qty, src, dest in moves:
        if not multiple or qty == 1:
            for _ in range(qty):
                stacks[dest - 1].append(stacks[src - 1].pop())
        else:
            tmp = deque()
            for _ in range(qty):
                tmp.append(stacks[src - 1].pop())
            while tmp:
                stacks[dest - 1].append(tmp.pop())
    return ''.join(stack[-1] for stack in stacks)

crates, moves = map(lambda s: s.rstrip(), open('input.txt').read().split('\n\n'))
moves = [tuple(map(int, move.strip().split()[1::2])) for move in moves.split('\n')]
stacks = make_stacks(crates.split('\n'))
print(rearrange([deque(stack) for stack in stacks], moves))
print(rearrange(stacks, moves, True))
