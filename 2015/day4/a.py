from sys import argv
from hashlib import md5

with open(argv[1]) as fp:
    lines = fp.readlines()

def hash(guess: str) -> str:
    s = bytes(guess, 'utf-8')
    m = md5()
    m.update(s)
    return m.hexdigest()

def mine(key: str, prefix: str) -> int:
    i = 0
    while True:
        h = hash(key + str(i))
        if h.startswith(prefix):
            return i
        i += 1

print('\n'.join(list(map(str, (mine(key.strip(), '00000') for key in lines)))))
print('\n'.join(list(map(str, (mine(key.strip(), '000000') for key in lines)))))
