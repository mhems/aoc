from sys import argv

def parse() -> ({str: (int, {str})}):
    adj = dict()
    for line in open(argv[1]).readlines():
        tokens = line.strip().replace('=', ' ').replace(';', '').split()
        adj[tokens[1]] = tokens[5], set(''.join(tokens[10:]).split(','))
    return adj

def find_max_pressure(graph: {str: (int, {str})}, time: int = 30) -> int:
    return 0

graph = parse()
print(find_max_pressure(graph))
