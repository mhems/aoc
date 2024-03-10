from sys import argv
from collections import Counter
from functools import reduce

chunks = open(argv[1]).read().strip().split('\n\n')
print(sum(len(counter) for counter in (Counter(''.join(chunk.split('\n'))) for chunk in chunks)))
print(sum(len(list(reduce(lambda a, b: set(a).intersection(set(b)), chunk.split('\n')))) for chunk in chunks))
