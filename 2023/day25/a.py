import sys
import networkx as nx
from math import prod

graph = nx.Graph(dict( (lambda a, b: (a, set(b.split()))) (*line.rstrip().split(': '))
                      for line in open(sys.argv[1]).readlines()))
#nx.drawing.nx_pydot.write_dot(graph, "graph.dot")
print(prod(map(len, nx.stoer_wagner(graph)[1])))
