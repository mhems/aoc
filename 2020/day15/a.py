from sys import argv
from collections import defaultdict, deque

def play_game(nums: [int], n: int) -> int:
    memory = defaultdict(list)
    spoken = deque()
    for i, num in enumerate(nums):
        memory[num].append(i)
        lastSpoken = num
        spoken.append(lastSpoken)
    for i in range(len(nums), n):
        if len(memory[lastSpoken]) <= 1:
            lastSpoken = 0
        else:
            lastSpoken = memory[lastSpoken][-1] - memory[lastSpoken][-2]
        memory[lastSpoken].append(i)
        spoken.append(lastSpoken)
    #print(spoken)
    return lastSpoken

nums = [list(map(int, line.strip().split(','))) for line in open(argv[1]).readlines()]
for seq in nums:
    print(play_game(seq, 2020))
    #print(play_game(seq, 30_000_000))
