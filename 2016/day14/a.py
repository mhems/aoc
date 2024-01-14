from sys import argv
from hashlib import md5
import re

regex = re.compile(r'(.)\1\1')

with open(argv[1]) as fp:
    salt = fp.read().strip()

def hash(salt: str, index: int, stretch=0) -> str:
    s = salt + str(index)
    for _ in range(stretch + 1):
        m = md5()
        m.update(bytes(s, 'utf-8'))
        s = m.hexdigest().lower()
    return s

def is_key(salt: str, index: int, hashes: [str]) -> str:
    if index + 1000 >= len(hashes):
        raise ValueError(index)
    hash_ = hashes[index]
    match = re.search(regex, hash_)
    if match:
        sub = 5 * match.groups(1)[0]
        for cand in hashes[index+1: index+1+1000]:
            if sub in cand:
                return hash_
    return None

def find_keys(salt: str, amt: int, hashes: [str]) -> [(int, str)]:
    keys = []
    index = 0
    while len(keys) < amt:
        key = is_key(salt, index, hashes)
        if key is not None:
            keys.append((index, key))
        index += 1
    return keys

hashes = [hash(salt, i) for i in range(50_000)]
print(find_keys(salt, 64, hashes)[-1][0])

stretched_hashes = []
for i in range(50_000):
    stretched_hashes.append(hash(salt, i, 2016))
    if i and i % 5_000 == 0:
        print('.', end='', flush=True)
    i += 1
print()
print(find_keys(salt, 64, stretched_hashes)[-1][0])
