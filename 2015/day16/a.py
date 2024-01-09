from sys import argv

with open(argv[1]) as fp:
    text = fp.read()
    
traits, memories = text.strip().split('\n\n')
traits = traits.split('\n')
memories = memories.split('\n')

def parse_trait(line: str) -> (str, int):
    k, v = line.strip().split(': ')
    return k, int(v)

traits = {k : v for k, v in map(parse_trait, traits)}

def parse_traits(line: str) -> (str, {str: int}):
    sep = line.index(':')
    name = line[:sep]
    return name, {k: v for k, v in map(parse_trait, line[sep+2:].split(','))}

memories = {name: (d, True) for name, d in map(parse_traits, memories)}

for k, v in traits.items():
    for sue, (d, ok) in memories.items():
        if ok:
            if k in d:
                memories[sue] = (d, d[k] == v)

print([name for name, (_, ok) in memories.items() if ok])

memories = {k : (d, True) for k, (d, _) in memories.items()}
for k, v in traits.items():
    for sue, (d, ok) in memories.items():
        if ok:
            if k in d:
                if k in ('cats', 'trees'):
                    memories[sue] = (d, d[k] > v)
                elif k in ('pomeranians', 'goldfish'):
                    memories[sue] = (d, d[k] < v)
                else:
                    memories[sue] = (d, d[k] == v)

print([name for name, (_, ok) in memories.items() if ok])