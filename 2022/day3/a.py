from functools import reduce

def total_priority(itr) -> int:
    def in_common(es) -> str:
        return reduce(lambda s1, s2: set(s1).intersection(set(s2)), es).pop()
    def priority(s: str) -> int:
        return ord(s) - ord('a') + 1 if s.islower() else ord(s) - ord('A') + 27
    return sum(priority(in_common(e)) for e in itr)

lines = [line.strip() for line in open('input.txt').readlines()]
rucks = [(line[:len(line)//2], line[len(line)//2:]) for line in lines]
print(total_priority(rucks))

badges = [lines[i:i+3] for i in range(0, len(lines) - 2, 3)]
print(total_priority(badges))
