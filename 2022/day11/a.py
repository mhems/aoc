from sys import argv
from math import prod
from collections import deque

class Monkey():
    def __init__(self, id: int, items: [int], operation: str, divisor: int, left_id: int, right_id: int):
        self.id = id
        self.items = deque(items)
        self.equation = operation
        self.operation = lambda old: eval(operation)
        self.test = lambda x: x % divisor == 0
        self.divisor = divisor
        self.throws = (right_id, left_id)
        self.inspect_count = 0
        self.modulus = None
    
    def __str__(self) -> str:
        return str((self.id, self.items, self.equation, self.divisor, self.throws, self.inspect_count))
    
    def turn(self, monkeys: list, divisor: int = 3):
        if self.modulus is None:
            self.modulus = prod(monkey.divisor for monkey in monkeys)
        if self.items:
            while self.items:
                val = self.operation(self.items.popleft())
                if divisor > 1:
                    val //= divisor
                else:
                    val %= self.modulus
                dest = int(self.test(val))
                monkeys[self.throws[dest]].items.append(val)
                self.inspect_count += 1

def parse(lines: [str]) -> Monkey:
    def last_token_as_int(line: str) -> int:
        return int(line.strip().split()[-1])
    id = last_token_as_int(lines[0].strip().rstrip(':'))
    items = list(map(int, lines[1].strip().split(': ')[1].split(', ')))
    operation = lines[2].strip().split(' = ')[1]
    divisor = last_token_as_int(lines[3])
    left = last_token_as_int(lines[4])
    right = last_token_as_int(lines[5])
    return Monkey(id, items, operation, divisor, left, right)

def round(monkeys: [Monkey], divisor: int = 3):
    for monkey in monkeys:
        monkey.turn(monkeys, divisor)

def game(monkeys: [Monkey], n: int = 20, divisor: int = 3):
    for _ in range(n):
        round(monkeys, divisor)
    return prod(sorted((monkey.inspect_count for monkey in monkeys), reverse=True)[:2])

monkeys = [parse(chunk.split('\n')) for chunk in open(argv[1]).read().split('\n\n')]
print(game(monkeys))
monkeys = [parse(chunk.split('\n')) for chunk in open(argv[1]).read().split('\n\n')]
print(game(monkeys, 10000, 1))
