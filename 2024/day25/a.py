from sys import argv

def parse() -> ({int}, {int}):
    def inner(text: str) -> (bool, (int)):
        lines = [line.strip() for line in text.strip().split('\n')]
        heights = []
        lock = False
        if all(c == '#' for c in lines[0]):
            lock = True
            for col in range(5):
                row = 1
                while row < 7 and lines[row][col] == '#':
                    row += 1
                heights.append(row - 1)
        elif all(c == '#' for c in lines[-1]):
            for col in range(5):
                row = 5
                while row > 0 and lines[row][col] == '#':
                    row -= 1
                heights.append(5 - row)
        else:
            raise ValueError()
        return lock, tuple(heights)
    keys, locks = set(), set()
    for block in open(argv[1]).read().split('\n\n'):
        is_lock, heights = inner(block.strip())
        if is_lock:
            locks.add(heights)
        else:
            keys.add(heights)
    return keys, locks

def valid_pairs(keys: (int), locks: (int)) -> int:
    return sum(int(all(e1 + e2 < 6 for e1, e2 in zip(key, lock))) for lock in locks for key in keys)

keys, locks = parse()
print(valid_pairs(keys, locks))
