from sys import argv
from math import log, ceil

def snafu_to_decimal(num: str) -> int:
    place = 1
    i = len(num) - 1
    decimal = 0
    while i >= 0:
        v = num[i]
        if v.isdigit():
            decimal += int(v) * place
        else:
            f = -1 if v == '-' else -2
            decimal += f * place
        i -= 1
        place *= 5
    return decimal

def decimal_to_penta(num: int) -> str:
    digits = []
    num_digits = ceil(log(num, 5))
    place = 5 ** num_digits
    while place > 0:
        d = num // place
        digits.append(str(d))
        num -= d * place
        place //= 5
    return ''.join(digits).lstrip('0')

def decimal_to_snafu(num: int) -> str:
    def snafu_increment(n: str) -> str:
        if n == '-':
            return '0'
        if n == '=':
            return '-'
        return str(int(n) + 1)
    digits = list(reversed(decimal_to_penta(num)))
    for i, d in enumerate(digits):
        v = int(d)
        if v in (3, 4):
            digits[i] = '-' if v == 4 else '='
            digits[i+1] = snafu_increment(digits[i+1])
        elif v > 4:
            assert v == 5
            digits[i] = '0'
            digits[i+1] = snafu_increment(digits[i+1])
    return ''.join(reversed(digits))
    
total = sum(snafu_to_decimal(line.strip()) for line in open(argv[1]).readlines())
print(decimal_to_snafu(total))
