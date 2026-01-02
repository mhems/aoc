import sys
from collections import deque
import networkx as nx

dirs = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}

class State:
    def __init__(self, grid_pos: tuple[int, int], regex_pos: int):
        self.grid_pos = grid_pos
        self.regex_pos = regex_pos
        self.alternations = set()
    def visit(self, regex: str, state_stack, new_states, edges):
        if self.regex_pos >= len(regex):
            return
        if regex[self.regex_pos] == '(':
            # add our grid position so future alternatives know where to start from
            state_stack.append(self.grid_pos)
            self.regex_pos += 1
            new_states.add(self)
        elif regex[self.regex_pos] == '|':
            # create new state for this alternation, starting where we were at last '('
            new_state = State(state_stack[-1], self.regex_pos + 1)
            new_states.add(new_state)
            # add current state to be resumed once we reach ')'
            self.alternations.add(self.grid_pos)
        elif regex[self.regex_pos] == ')':
            _ = state_stack.pop()
            # add this as the last alternation
            self.alternations.add(self.grid_pos)
            # resurrect all alternatives to pick up at current regex pos but their grid pos
            for alt_pos in self.alternations:
                new_states.add(State(alt_pos, self.regex_pos + 1))
            self.alternations.clear()
        else:
            new_pos = tuple(map(sum, zip(self.grid_pos, dirs[regex[self.regex_pos]])))
            if (new_pos, self.grid_pos) not in edges:
                edges.add((self.grid_pos, new_pos))
            self.grid_pos = new_pos
            self.regex_pos += 1
            new_states.add(self)

def walk(regex: str):
    state_stack = deque(((0, 0), ))
    states = {State((0, 0), 0)}
    edges = set()
    while states:
        new_states = set()
        for state in states:
            state.visit(regex, state_stack, new_states, edges)
        states = new_states
    return nx.DiGraph(edges)

regex = open(sys.argv[1]).read().strip()[1:-1]
graph = walk(regex)
#nx.drawing.nx_pydot.write_dot(graph, sys.argv[1].split('.')[0] + ".dot")
print(nx.dag_longest_path_length(graph), flush=True)
print(sum(int(len(path[0]) >= 1001) for _, path in (nx.single_source_all_shortest_paths(graph, (0, 0)))))
