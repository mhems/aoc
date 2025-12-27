import sys
import networkx as nx

adj_list = dict((lambda a, b: (a, set(b.split()))) (*line.rstrip().split(': '))
                for line in open(sys.argv[1]).readlines())

def make_dot_file():
    print("digraph G {")
    for node, neighbors in adj_list:
        for neighbor in neighbors:
            print(f"  {node} -> {neighbor};")
    print("}")

# make_dot_file()
# sys.exit(0)

G = nx.DiGraph(adj_list)
assert nx.is_directed_acyclic_graph(G)

def count_paths_dag(G, source, target):
    paths = {node: 0 for node in G.nodes()}
    paths[source] = 1
    for u in nx.topological_sort(G):
        for v in G.successors(u):
            paths[v] += paths[u]
    return paths[target]

print(count_paths_dag(G, 'you', 'out'))

dac_to_fft = count_paths_dag(G, 'dac', 'fft')
fft_to_dac = count_paths_dag(G, 'fft', 'dac')
if dac_to_fft > 0:
    a, b = 'dac', 'fft'
    middle = dac_to_fft
else:
    a, b = 'fft', 'dac'
    middle = fft_to_dac
print(count_paths_dag(G, 'svr', a) * middle * count_paths_dag(G, b, 'out'))
