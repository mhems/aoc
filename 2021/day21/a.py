from sys import argv
from itertools import cycle
from collections import defaultdict

def deterministic_play(p1: int, p2: int) -> int:
    ps = [p1 - 1, p2 - 1]
    scores = [0, 0]
    die = cycle(range(1, 101))
    num_rolls = 0
    while True:
        for i in (0, 1):
            val = sum((next(die), next(die), next(die)))
            num_rolls += 3
            ps[i] = (ps[i] + val) % 10
            scores[i] += ps[i] + 1
            if scores[i] >= 1000:
                return min(scores) * num_rolls

def take_turn(game_states: {((int, int), (int, int)): int}, winners: [int, int], player: int) -> {((int, int), (int, int)): int}:
    chances = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    new_states = defaultdict(int)
    for game, game_freq in game_states.items():
        for total, freq in chances.items():
            pos = (game[player][0] + total) % 10
            score = game[player][1] + pos + 1
            if score >= 21:
                winners[player] += freq * game_freq
            else:
                state = ((pos, score), game[1]) if player == 0 else (game[0], (pos, score))
                new_states[state] += freq * game_freq
    return new_states

def quantum_play(p1: int, p2: int) -> int:
    game_states = {((p1-1, 0), (p2-1, 0)): 1}
    winners = [0, 0]
    while game_states:
        game_states = take_turn(game_states, winners, 0)
        game_states = take_turn(game_states, winners, 1)
    return max(winners)

p1, p2 = [int(line.strip().split()[-1]) for line in open(argv[1]).readlines()]
print(deterministic_play(p1, p2))
print(quantum_play(p1, p2))