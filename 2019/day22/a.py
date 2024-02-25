from sys import argv

def reverse(deck: [int]) -> [int]:
    return list(reversed(deck))

def cut(deck: [int], n: int) -> [int]:
    return deck[n:] + deck[:n]

def deal(deck: [int], n: int) -> [int]:
    new_deck = [None] * len(deck)
    i = 0
    for e in deck:
        new_deck[i % len(deck)] = e
        i += n
    return new_deck

def shuffle(commands: [str], deck=None) -> [int]:
    if deck is None:
        deck = list(range(10007))
    for command in commands:
        tokens = command.split()
        if tokens[0] == 'cut':
            deck = cut(deck, int(tokens[-1]))
        elif tokens[1] == 'with':
            deck = deal(deck, int(tokens[-1]))
        else:
            deck = reverse(deck)
    return deck

def long_shuffle(commands: [str], n=101741582076661, pos=2020):
    deck = list(range(119315717514047))
    for i in range(n):
        deck = shuffle(commands, deck)
    return deck

commands = [line.strip() for line in open(argv[1]).readlines()]
print(shuffle(commands).index(2019))
print(long_shuffle(commands)[2020])
