   
def get_cal_value(line: str) -> int:
    line = line.strip()
    left = None
    right = None
    for ch in line:
        if ch.isdigit():
            left = int(ch)
            break
    for ch in reversed(line):
        if ch.isdigit():
            right = int(ch)
            break
    return left * 10 + right

with open('input.txt') as fp:
   answer = sum(map(get_cal_value, fp.readlines()))
print(answer)
