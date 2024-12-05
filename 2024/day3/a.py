import re
from sys import argv
from operator import mul

regex = re.compile(r'mul\((\d+),(\d+)\)|don\'t\(\)|do\(\)')
text = open(argv[1]).read()
total_prod = 0
enabled_prod = 0
enabled = True
for match in re.finditer(regex, text):
    if match[0].startswith('m'):
        product = mul(*map(int, match.group(1, 2)))
        total_prod += product
        if enabled:
            enabled_prod += product
    else:
        enabled = match[0][2] != 'n'

print(total_prod)
print(enabled_prod)
