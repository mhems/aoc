from sys import argv

def valid(passport: {str: str}) -> bool:
    byr = 1920 <= int(passport['byr']) <= 2002
    iyr = 2010 <= int(passport['iyr']) <= 2020
    eyr = 2020 <= int(passport['eyr']) <= 2030
    hgt, units = passport['hgt'][:-2], passport['hgt'][-2:]
    valid_height = (units == 'cm' and 150 <= int(hgt) <= 193) or (units == 'in' and 59 <= int(hgt) <= 76)
    hcl = passport['hcl'][0] == '#' and 6 == sum(1 for d in passport['hcl'] if d.isdigit() or d in 'abcdef')
    ecl = passport['ecl'] in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')
    pid = 9 == sum(1 for d in passport['pid'] if d.isdigit())
    return byr and iyr and eyr and valid_height and hcl and ecl and pid

chunks = [dict(item.split(':') for item in ' '.join(chunk.split('\n')).split())
          for chunk in open(argv[1]).read().strip().split('\n\n')]
sized = [chunk for chunk in chunks if len(chunk) == 8 or len(chunk) == 7 and 'cid' not in chunk]
print(len(sized))
print(sum(int(valid(chunk)) for chunk in sized))
