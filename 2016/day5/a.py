from sys import argv
from hashlib import md5

with open(argv[1]) as fp:
    door = fp.read().strip()

def generate_password1(door: str) -> str:
    password = ''
    i = 0
    while len(password) != 8:
        s = bytes(door + str(i), 'utf-8')
        m = md5()
        m.update(s)
        hash = m.hexdigest()
        if hash.startswith('00000'):
            password += hash[5]
        i += 1
    return password

def generate_password2(door: str) -> str:
    password = [None] * 8
    i = 0
    while any(e == None for e in password):
        s = bytes(door + str(i), 'utf-8')
        m = md5()
        m.update(s)
        hash = m.hexdigest()
        if hash.startswith('00000'):
            #print(hash)
            pos = int(hash[5], 16)
            if pos < 8 and password[pos] is None:
                password[pos] = hash[6]
        i += 1
    return ''.join(password)

print(generate_password1(door))
print(generate_password2(door))
