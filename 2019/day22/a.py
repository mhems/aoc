from sys import argv

class Deck:
    def __init__(self, n: int):
        self.n = n
        self.a = 1
        self.b = 0
    def rotate(self, amt: int):
        self.b = (self.b - amt) % self.n
    def increment(self, amt: int):
        self.a = (self.a * amt) % self.n
        self.b = (self.b * amt) % self.n
    def reverse(self):
        self.a = -self.a % self.n
        self.b = (-self.b - 1) % self.n

k = 101_741_582_076_661
d1 = Deck(10_007)
d2 = Deck(119_315_717_514_047)

for line in open(argv[1]).readlines():
    tokens = line.strip().split()
    if tokens[0] == 'cut':
        amt = int(tokens[-1])
        d1.rotate(amt)
        d2.rotate(amt)
    elif tokens[1] == 'with':
        amt = int(tokens[-1])
        d1.increment(amt)
        d2.increment(amt)
    else:
        d1.reverse()
        d2.reverse()

def evaluate(a: int, b: int, n: int, x: int) -> int:
    return (a*x + b) % n

def inverse(b, p) -> int:
    return pow(b, p-2, p)

def exponentiate(a, b, k, p) -> tuple[int, int]:
    coeff = pow(a, k, p)
    const = (b * (coeff-1) * inverse(a-1, p)) % p
    return coeff, const

def invert(a, b, p):
    a_inv = inverse(a, p)
    b *= -a_inv
    return a_inv, b

print(evaluate(d1.a, d1.b, d1.n, 2019))

a, b = exponentiate(d2.a, d2.b, k, d2.n)
a, b = invert(a, b, d2.n)
print(evaluate(a, b, d2.n, 2020))
