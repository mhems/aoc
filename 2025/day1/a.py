import sys

pos = 50
num_end_on_zero = 0
num_thru_zero = 0

for rot in open(sys.argv[1]).readlines():
    sign = 2 * int(rot[0] == 'R') - 1
    magnitude = int(rot[1:])
    amt = sign * magnitude
    quot, rem = divmod(magnitude, 100)    
    raw_sum = pos + sign * rem
    num_thru_zero += quot + int((sign < 0 and raw_sum < 0) or raw_sum > 100 or pos == 0)
    pos = raw_sum % 100
    num_end_on_zero += int(pos == 0)

print(num_end_on_zero)
print(num_thru_zero)
