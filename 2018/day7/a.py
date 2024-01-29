from sys import argv

with open(argv[1]) as fp:
    lines = fp.readlines()

def parse_dep(line) -> (str, str):
    tokens = line.strip().split()
    return tokens[1], tokens[-3]

def make_adj(steps: [str], deps: [(int, int)]) -> {str: [str]}:
    adj = {step: [] for step in steps}
    for dep in deps:
        adj[dep[0]].append(dep[1])  
    return adj

def make_incidences(steps: [str], deps: [(int, int)]) -> {str: [str]}:
    inc = {step: [] for step in steps}
    for dep in deps:
        inc[dep[1]].append(dep[0])
    return inc

def get_starts(steps: [str], adj: {str: [str]}) -> {str}:
    afters = set()
    for v in adj.values():
        for e in v:
            afters.add(e)
    return steps - afters

def alphabetic_bfs(steps: [str], deps: [(str, str)]) -> str:
    visited = ''
    adj = make_adj(steps, deps)
    inc = make_incidences(steps, deps)
    queue = get_starts(steps, adj)
    while len(queue) > 0:
        cur = None
        while cur is None:
            for step in sorted(queue):
                if all(n in visited for n in inc[step]):
                    cur = step
                    break
        queue.remove(cur)
        visited += cur
        for n in adj[cur]:
            queue.add(n)
    return visited

def concurrent_bfs(steps: [str], deps: [(str, str)], num_workers: int = 5, base_time: int = 60) -> str:
    visited = ''
    workers = [None] * num_workers
    times = [None] * num_workers
    adj = make_adj(steps, deps)
    inc = make_incidences(steps, deps)
    queue = get_starts(steps, adj)
    duration = 0
    while len(visited) < len(steps):
        for step in sorted(queue):
            if all(n in visited for n in inc[step]):
                if None in workers:
                    i = workers.index(None)
                    workers[i] = step
                    queue.remove(step)
                    times[i] = base_time + ord(step) - ord('A') + 1
                else:
                    break
        for worker in workers:
            if worker is not None:
                for n in adj[worker]:
                    queue.add(n)
        for i, time in enumerate(times):
            if time is not None:
                times[i] -= 1
                if times[i] == 0:
                    visited += workers[i]
                    workers[i] = None
                    times[i] = None
        duration += 1
    return visited, duration

deps = [parse_dep(line.strip()) for line in lines]
steps = {dep[0] for dep in deps}.union({dep[1] for dep in deps})
print(alphabetic_bfs(steps, deps))
print(concurrent_bfs(steps, deps))
