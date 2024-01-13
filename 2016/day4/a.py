from sys import argv
import re
from collections import Counter

with open(argv[1]) as fp:
    lines = fp.readlines()

regex = re.compile(r'([a-z]+(?:-[a-z]+)*)-([0-9]+)\[([a-z]+)\]', re.I)

def parse_line(line: str) -> (str, str):
    match = re.match(regex, line)
    if match:
        return tuple(match.groups())

def compute_checksum(cipher: str) -> str:
    counter = Counter(cipher)
    rev = {}
    for char, freq in counter.items():
        if freq not in rev:
            rev[freq] = ''
        rev[freq] += char
    checksum = ''
    for freq in sorted(rev.keys(), reverse=True):
        checksum += ''.join(sorted(rev[freq]))
        if len(checksum) >= 5:
            return checksum[:5]
    return checksum

def validate(cipher: str, sector: str, checksum: str) -> int:
    live = compute_checksum(cipher.replace("-", ""))
    #print(cipher, ':', live, 'vs', checksum)
    return int(sector) if checksum == live else 0

codes = [parse_line(line.strip()) for line in lines]
print(sum(validate(*code) for code in codes))

def decrypt(cipher: str, sector: str, _: str) -> str:
    shift = int(sector)
    def decrypt_chunk(chunk: str) -> str:
        return ''.join(chr(ord('a') + (ord(char) - ord('a') + shift) % 26) for char in chunk)
    return ' '.join(decrypt_chunk(token) for token in cipher.split('-'))

rooms = [(code[1], decrypt(*code)) for code in codes]
for num, room in rooms:
    if 'pole' in room:
        print(num, room)
