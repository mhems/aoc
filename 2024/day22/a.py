from sys import argv
from collections import defaultdict

def evolve(n: int,) -> int:
    n ^= n * 64
    n %= 16777216
    n ^= n // 32
    n %= 16777216
    n ^= n * 2048
    n %= 16777216
    return n

def get_prices(initial: int, amt: int) -> (int, [int], [int]):
    n = initial
    ret = [n % 10]
    changes = []
    for _ in range(amt):
        last = n % 10
        n = evolve(n)
        e = n % 10
        changes.append(e - last)
        ret.append(e)
    return n, ret, changes

def get_quad_runs(prices: [int], deltas: [int]) -> [(int, (int, int, int, int))]:
    return [(prices[i+4], tuple([deltas[i], deltas[i+1], deltas[i+2], deltas[i+3]])) for i in range(len(deltas) - 3)]

def best_quad(numbers: [int], amt: int = 2000) -> (int, int):
    total = 0
    quad_to_scores = defaultdict(int)
    for number in numbers:
        secret, prices, deltas = get_prices(number, amt)
        quads = get_quad_runs(prices, deltas)
        seen = set()
        for price, quad in quads:
            if quad not in seen:
                quad_to_scores[quad] += price
                seen.add(quad)
        total += secret
    _, profit = max(quad_to_scores.items(), key=lambda pair: pair[1])
    return total, profit

numbers = [int(line.strip()) for line in open(argv[1]).readlines()]
print(best_quad(numbers))
