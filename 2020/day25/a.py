from sys import argv

def transform(subject: int, loop_size: int) -> int:
    value = 1
    for _ in range(loop_size):
        value *= subject
        value %= 20201227
    return value
        
def brute_force(keys: (int, int), subject: int = 7) -> (int, int):
    answers = [None, None]
    loop_size = 1
    value = 1
    while True:
        value *= subject
        value %= 20201227
        if value == keys[0]:
            answers[0] = loop_size
            if answers[1] is not None:
                return tuple(answers)
        elif value == keys[1]:
            answers[1] = loop_size
            if answers[0] is not None:
                return tuple(answers)
        loop_size += 1

card_pub, door_pub = [int(line.strip()) for line in open(argv[1]).readlines()]
card_loop, door_loop = brute_force((card_pub, door_pub))
ek = transform(door_pub, card_loop)
print(ek)
