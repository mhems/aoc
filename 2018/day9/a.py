from sys import argv

def parse_line(line: str) -> (int, int):
    tokens = line.strip().split()
    return int(tokens[0]), int(tokens[-2])

def simulate(num_players: int, num_marbles: int) -> int:
    scores = [0] * num_players
    ring = [0, 1]
    current_index = 1
    for i in range(2, num_marbles + 1):
        if i % 23 == 0:
            remove_index = (current_index - 7) % len(ring)
            scores[(i - 1) % num_players] += i + ring.pop(remove_index)
            current_index = remove_index
        else:
            if current_index == len(ring) - 2:
                insert_index = len(ring)
            else:
                insert_index = (current_index + 2) % len(ring)
            ring.insert(insert_index, i)
            current_index = insert_index
        #print(i, (i-1) % num_players, ring)
    return max(scores)

with open(argv[1]) as fp:
    lines = fp.readlines()

pairs = [parse_line(line.strip()) for line in lines]

for num_players, num_marbles in pairs:
    print(simulate(num_players, num_marbles))
