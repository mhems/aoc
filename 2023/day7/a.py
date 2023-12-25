from sys import argv
from collections import namedtuple as nt
from itertools import combinations
    
def order_cards(str) -> str:
    return ''.join(sorted(str))

cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

def card_value(card: str) -> int:
    return len(cards) - cards.index(card)

def generate_five_kind() -> [str]:
    for card in cards:
        yield card * 5
        
def generate_four_kind() -> [str]:
    for c1 in cards:
        for c2 in cards:
            if c1 == c2:
                continue
            yield order_cards(c1 * 4 + c2)
            
def generate_full_house() -> [str]:
    for major in cards:
        for minor in cards:
            if major == minor:
                continue
            yield order_cards(major * 3 + minor * 2)
            
def generate_three_kind() -> [str]:
    for major in cards:
        remaining = list(cards)
        remaining.remove(major)
        for others in combinations(remaining, 2):
            yield order_cards(major * 3 + ''.join(others))
        #for fourth in cards:
        #    for fifth in cards:
        #        if major == fourth or major == fifth or card_value(fourth) <= card_value(fifth):
        #            continue
        #        yield order_cards(major * 3 + fourth + fifth)

def generate_two_pair() -> [str]:
    for a in cards:
        for b in cards:
            for fifth in cards:
                if card_value(a) <= card_value(b) or a == fifth or b == fifth:
                    continue
                yield order_cards(a * 2 + b * 2 + fifth)
                
def generate_pair() -> [str]:
    for a in cards:
        remaining = list(cards)
        remaining.remove(a)
        for others in combinations(remaining, 3):
            yield order_cards(a * 2 + ''.join(others))
            
def generate_high() -> [str]:
    for others in combinations(cards, 5):
        yield order_cards(''.join(others))
            
best = [
    generate_five_kind(),
    generate_four_kind(),
    generate_full_house(),
    generate_three_kind(),
    generate_two_pair(),
    generate_pair(),
    generate_high(),
]

#l = list(best[3])
#print(l[:30])
#print(l[-30:])
#None.list()

rank = 1
mapping = {}
for category in best:
    for hand in category:
        mapping[hand] = rank
        rank += 1

with open(argv[1]) as fp:
    lines = fp.readlines()

hands = []
for line in lines:
    left, right = line.strip().split()[:2]
    cards = order_cards(left)
    bid = int(right)
    hands.append((cards, bid))

ranked_hands = []
for hand, bid in hands:
    rank = mapping[hand]
    ranked_hands.append((hand, rank, bid))
    
ranked_hands.sort(key=lambda hand: hand[1], reverse=True)
#print(ranked_hands)
answer = sum(bid * (rank+1) for rank, (h, r, bid) in enumerate(ranked_hands))

for rank, (h, r, bid) in enumerate((ranked_hands)):
    print('%s (%d): $%d * %d = $%d' % (h, r, bid, rank+1, bid * (rank+1)))

print(answer)
