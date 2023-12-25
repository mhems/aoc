from sys import argv
from functools import cmp_to_key
from collections import Counter, OrderedDict

cards = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']

def card_value(card: str) -> int:
    return len(cards) - cards.index(card)

def get_plain_type(hand: str) -> int:
    counter = Counter(hand)
    sorted_freqs = sorted(((k, v) for k, v in counter.items()),
                          key=lambda pair: pair[1],
                          reverse=True)
    n = len(sorted_freqs)
    if n == 1:
        return 7
    elif n == 2:
        if sorted_freqs[0][1] == 4:
            return 6
        return 5
    elif n == 3:
        if sorted_freqs[0][1] == 3:
            return 4
        return 3
    elif n == 4:
        return 2
    return 1

def get_type(hand: str) -> int:
    if 'J' not in hand:
        return get_plain_type(hand)
    counter = Counter(hand)
    sorted_freqs = sorted(((k, v) for k, v in counter.items()),
                          key=lambda pair: pair[1],
                          reverse=True)
    n = len(sorted_freqs)
    if n <= 2:
        return 7
    elif n == 3:
        # 3 of a kind promotes to 4 of a kind if J is a kicker
        if sorted_freqs[0][1] == 3:
            return 6
        # 2 pair promotes to full house if J is kicker
        if 'J' == sorted_freqs[2][0]:
            return 5
        # 2 pair promotes to 4 of a kind if J is a pair
        return 6
    elif n == 4:
        return 4
    # high card always promotes to one pair
    return 2

def compare_hands(h1: str, h2: str) -> int:
    t1 = get_type(h1[0])
    t2 = get_type(h2[0])
    if t1 != t2:
        return t2 - t1
    for c1, c2 in zip(list(h1[0]), list(h2[0])):
        v1 = card_value(c1)
        v2 = card_value(c2)
        if v1 != v2:
            return v2 - v1
    return 0

with open(argv[1]) as fp:
    lines = fp.readlines()

hands = []
for line in lines:
    left, right = line.strip().split()[:2]
    bid = int(right)
    hands.append((left, bid))
    
hands.sort(key=cmp_to_key(compare_hands), reverse=True)
answer = sum(bid * (rank+1) for rank, (_, bid) in enumerate(hands))

for rank, (h, bid) in enumerate((hands)):
    print('%s: $%d * %d = $%d' % (h, bid, rank+1, bid * (rank+1)))

print(answer)
