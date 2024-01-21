from sys import argv

n = int(argv[1])
step_size = int(argv[2])

def run(n: int, step_size: int) -> int:
    buffer = [0]
    pos = 0
    for i in range(1, n + 1):
        pos = (pos + step_size) % len(buffer)
        pos += 1
        buffer.insert(pos, i)
    return buffer[pos + 1]

print(run(n, step_size))
