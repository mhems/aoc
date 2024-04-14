result = {(0, 0): 3, (0, 1): 0, (0, 2): 6, (1, 0): 6, (1, 1): 3, (1, 2): 0, (2, 0): 0, (2, 1): 6, (2, 2): 3}
directions = [tuple(line.strip().split()) for line in open('input.txt').readlines()]

def play(directions: [(str, str)]) -> (int, int):
    moves = {(v, them): me for (me, them), v in result.items()}
    exact_score, cheat_score = 0, 0
    for opponent, me in directions:
        my_index = ord(me) - ord('X')
        their_index = ord(opponent) - ord('A')
        exact_score += result[(my_index, their_index)] + my_index + 1
        cheat_score += my_index * 3 + moves[(my_index * 3, their_index)] + 1
    return exact_score, cheat_score

print(play(directions))
