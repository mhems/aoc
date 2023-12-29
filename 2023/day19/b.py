from sys import argv
from collections import namedtuple as nt
from functools import reduce
import operator
import pprint

with open(argv[1]) as fp:
    lines = fp.readlines()

Workflow = nt('Workflow', ['name', 'rules'])
Condition = nt('Condition', ['var', 'op', 'val'])
Rule = nt('Rule', ['condition', 'destination'])
Range = nt('Range', ['lower', 'upper'])

Connection = nt('Connection', ['conditions', 'vertex'])
Vertex = nt('Vertex', ['name', 'connections'])

def parse_condition(s: str) -> Condition:
    if '>' in s:
        var, right = s.split('>')
        return Condition(var, '>', int(right))
    if '<' in s:
        var, right = s.split('<')
        return Condition(var, '<', int(right))

def parse_rule(s: str) -> Rule:
    if ':' not in s:
        return Rule(None, s.strip())
    cond, state = s.split(':')
    return Rule(parse_condition(cond), state)

def parse_workflow(s: str) -> Workflow:
    name, right = s.split('{')
    rules = list(map(parse_rule, right.strip('}').split(',')))
    return Workflow(name, rules)

def negate(conditions: [Condition]) -> [Condition]:
    negations = []
    for condition in conditions:
        if condition is None:
            continue
        if condition.op == '>':
            op = '<'
            value = condition.val + 1
        else:
            op = '>'
            value = condition.val - 1
        negations.append(Condition(condition.var, op, value))
    return negations

def count(ranges: [Range]) -> int:
    return reduce(operator.mul, (r.upper - r.lower - 1 for r in ranges))

def consolidate(conditions: [Condition]) -> [Range]:
    ranges = [Range(0, 4001)] * len('xmas')
    for condition in conditions:
        i = 'xmas'.index(condition.var)
        if condition.op == '>':
            if condition.val > ranges[i].lower:
                ranges[i] = Range(condition.val, ranges[i].upper)
        else:
            if condition.val < ranges[i].upper:
                ranges[i] = Range(ranges[i].lower, condition.val)
    return ranges

def dfs(vertex: Vertex, visited: [Vertex], edges: [Condition], paths: [[Condition]]):
    if vertex.name == 'A':
        paths.append(edges)
        return
    if vertex.name == 'R':
        return
    if vertex in visited:
        return
    visited = list(visited) + [vertex]
    for connection in vertex.connections:
        dfs(connection.vertex,
            visited,
            list(edges) + connection.conditions,
            paths)

def build(workflows: {str: Workflow}) -> {str: Vertex}:
    vertices = {}
    for workflow in workflows.values():
        connections = []
        for i, rule in enumerate(workflow.rules):
            conditions = negate(rule.condition for rule in workflow.rules[:i])
            if rule.condition is not None:
                conditions.append(rule.condition)
            connections.append(Connection(conditions, rule.destination))
        vertex = Vertex(workflow.name, connections)
        vertices[vertex.name] = vertex
    vertices['A'] = Vertex('A', [])
    vertices['R'] = Vertex('R', [])
    for vertex in vertices.values():
        original = list(vertex.connections)
        vertex.connections.clear()
        for connection in original:
            vertex.connections.append(Connection(connection.conditions, vertices[connection.vertex]))
    return vertices

workflows = {}
for line in lines:
    if len(line.strip()) == 0:
        break
    workflow = parse_workflow(line.strip())
    workflows[workflow.name] = workflow

graph = build(workflows)
#pprint.pprint(graph['in'])
paths = []
dfs(graph['in'], [], [], paths)
#pprint.pprint(paths)
ranges = [consolidate(path) for path in paths]
#print(ranges)
counts = [count(e) for e in ranges]
#print(counts)
print(sum(counts))
