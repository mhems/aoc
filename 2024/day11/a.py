from sys import argv
from collections import defaultdict

freq = defaultdict(int)

class StoneNode:
    def __init__(self, a: int):
        self.left = a
        self.right = None
        freq[self.left] += 1

    def blink(self):
        if self.right is not None:
            self.left.blink()
            self.right.blink()
        elif self.left == 0:
            self.left = 1
        else:
            str_ = str(self.left)
            N = len(str_)
            if N % 2 == 0:
                self.left = StoneNode(int(str_[:N//2]))
                self.right = StoneNode(int(str_[N//2:]))
            else:
                self.left *= 2024
                
    def __str__(self) -> str:
        if self.right is not None:
            return f'({self.left}, {self.right})'
        return f'({self.left})'

    def flatten(self) -> int:
        flattened = []
        if self.right is not None:
            flattened.extend(self.left.flatten())
            flattened.extend(self.right.flatten())
        else:
            flattened.append(self.left)
        return flattened

    def count(self) -> int:
        flattened = 0
        if self.right is not None:
            flattened += self.left.count()
            flattened += self.right.count()
        else:
            flattened += 1
        return flattened

def optimized_blink_many(stones: [int], n: int) -> int:
    stones = [StoneNode(e) for e in stones]
    for i in range(n):
        for stone in stones:
            stone.blink()
        print('iteration', i, sum(stone.count() for stone in stones), sum(int(v > 1) for v in freq.values() if v > 1), flush=True)
    return sum(stone.count() for stone in stones)

stones = [int(stone) for stone in open(argv[1]).read().strip().split()]
print(optimized_blink_many(stones, 25))
