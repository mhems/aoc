from sys import argv

def safe(report: [int], tolerant: bool = False) -> bool:
    diffs = [a - b for a, b in zip(report[:-1], report[1:])]
    initial = (all(e > 0 for e in diffs) or all(e < 0 for e in diffs)) and all(1 <= abs(e) <= 3 for e in diffs)
    if initial or not tolerant:
        return initial
    for i in range(len(report)):
        copy = list(report)
        copy.pop(i)
        if safe(copy):
            return True
    return False

reports = [list(map(int, line.strip().split())) for line in open(argv[1]).readlines()]
print(sum(int(safe(report)) for report in reports))
print(sum(int(safe(report, True)) for report in reports))
