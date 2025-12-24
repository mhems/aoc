import sys

def max_joltage(bank: tuple[int], num_on: int = 2) -> int:    
    if num_on == 1:
        return max(bank)
    max_index = max(range(len(bank) - (num_on-1)), key=bank.__getitem__)
    return bank[max_index] * 10**(num_on-1) + max_joltage(bank[max_index+1:], num_on-1)

banks = [tuple(int(e) for e in bank.strip()) for bank in open(sys.argv[1]).readlines()]
print(sum(max_joltage(bank) for bank in banks))
print(sum(max_joltage(bank, 12) for bank in banks))
