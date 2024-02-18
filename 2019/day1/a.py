with open('input.txt') as fp:
    nums = [int(line.strip()) for line in fp.readlines()]

def fuel(n: int) -> int:
    return n//3 - 2

def fuel_recursive(n: int) -> int:
    f = fuel(n)
    if f <= 0:
        return 0
    return f + fuel_recursive(f)

print(sum(fuel(n) for n in nums))
print(sum(fuel_recursive(n) for n in nums))
