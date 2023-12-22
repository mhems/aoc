   
d = {
    'zero' : 0,
    'one' : 1,
    'two' : 2,
    'three' : 3,
    'four' : 4,
    'five' : 5,
    'six' : 6,
    'seven' : 7,
    'eight' : 8,
    'nine' : 9
}

def get_cal_value(line: str) -> int:
    line = line.strip()
    nums = []
    for i, ch in enumerate(line):
        if ch.isdigit():
            nums.append(int(ch))
            continue
        for key in d:
            if line[i:].startswith(key):
                nums.append(d[key])
                break
    return nums[0] * 10 + nums[-1]

with open('input.txt') as fp:
    answer = sum(map(get_cal_value, fp.readlines()))
print(answer)
