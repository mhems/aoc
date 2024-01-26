from sys import argv

n = int(argv[1])
step_size = int(argv[2])

def run(n: int, step_size: int) -> int:
    buf = None
    pos = 0
    for i in range(1, n + 1):
        pos = (pos + step_size) % i
        pos += 1
        if pos == 1:
            buf = i
    return buf

print(run(n, step_size))
