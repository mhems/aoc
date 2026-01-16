import sys
from typing import Iterable
from itertools import combinations
from collections import defaultdict, Counter, deque
import numpy as np

p = [(1, 2, 3), (1, -3, 2), (1, -2, -3), (1, 3, -2),
     (-1, -2, 3), (-1, -3, -2), (-1, 2, -3), (-1, 3, 2),
     (2, -1, 3), (2, -3, -1), (2, 1, -3), (2, 3, 1),
     (-2, 1, 3), (-2, -3, 1), (-2, -1, -3), (-2, 3, -1),
     (3, 2, -1), (3, -1, -2), (3, -2, 1), (3, 1, 2),
     (-3, 2, 1), (-3, 1, -2), (-3, -2, -1), (-3, -1, 2)]

def make_rotations() -> list[np.array]:
    rotations = []
    for rot in p:
        rotation = []
        for col in rot:
            ind = abs(col) - 1
            v = 1 if col > 0 else -1
            row = [0] * 3
            row[ind] = v
            rotation.append(row)
        rotations.append(np.array(rotation, dtype=np.int8))
    return rotations

rotations = make_rotations()

class Scanner:
    def __init__(self, id, points: np.array):
        self.id = id
        self.beacons = points
        self.ds = defaultdict(set)
        self.oriented = id == 0
        self.location = None if id != 0 else np.array([0, 0, 0], dtype=np.int32)
    def distances(self):
        if len(self.ds) == 0:
            for b1, b2 in combinations(self.beacons, 2):
                diff = b1 - b2
                self.ds[np.dot(diff, diff)].add(tuple(map(tuple, (b1, b2))))
    def place(self, rotation, translation):
        self.beacons = self.beacons @ rotation + translation
        self.oriented = True
        self.location = translation

class ScannerPair:
    def __init__(self, a_id: int, b_id: int):
        self.a_id, self.b_id = a_id, b_id
        self.count = 0
        self.a_beacons = set()
        self.b_beacons = set()
        self.by_distance = dict()
        self.associations = set()
    @property
    def a(self) -> Scanner:
        return scanners[self.a_id]
    @property
    def b(self) -> Scanner:
        return scanners[self.b_id]
    def __iter__(self) -> Iterable[Scanner]:
        yield self.a
        yield self.b
    def quantify_common(self) -> int:
        self.a.distances()
        self.b.distances()
        return len(self.a.ds.keys() & (self.b.ds.keys()))
    def collect_points_in_common(self):
        self.a.ds.clear()
        self.b.ds.clear()
        self.a.distances()
        self.b.distances()
        for distance, pairs in self.a.ds.items():
            other_pairs = self.b.ds.get(distance, [])
            if min(len(pairs), len(other_pairs)) > 0:
                assert len(pairs) == 1
                assert len(other_pairs) == 1
                a, b = pairs.pop(), other_pairs.pop()
                self.a_beacons.update(a)
                self.b_beacons.update(b)
                self.by_distance[distance] = (a, b)
    def associate_points(self):
        def find_pair(x: np.array):
            counter = Counter()
            for (a, b) in self.by_distance.values():
                if x in a:
                    for e in b:
                        counter[e] += 1
            p, amt = counter.most_common(1)[0]
            if amt >= 11:
                return p
            return None
        for x in self.a_beacons:
            y = find_pair(x)
            if y:
                self.associations.add((x, y))
        self.associations = list(self.associations)
        assert len(self.associations) == 12
        
        xs, ys = zip(*self.associations)
        self.a_matrix = np.array([tuple(x) for x in xs], dtype=np.int32)
        self.b_matrix = np.array([tuple(y) for y in ys], dtype=np.int32)
    def find_translation(self):      
        assert self.a.oriented
        assert not self.b.oriented

        for rotation in rotations:
            diff = self.a_matrix - self.b_matrix @ rotation
            if np.all(diff[0] == diff):
                self.b.place(rotation, diff[0])
                break
        else:
            assert False, 'unable to find rotation'

scanners = {i: Scanner(i, np.array([tuple(map(int, line.strip().split(',')))
                                    for line in chunk.split('\n')[1:]], dtype=np.int32))
            for i, chunk in enumerate(open(sys.argv[1]).read().strip().split('\n\n'))}
pairs = {(s1, s2): ScannerPair(s1, s2) for s1, s2 in combinations(scanners.keys(), 2)}

adj_list = defaultdict(set)
for pair in pairs.values():
    if pair.quantify_common() >= 66:
        s1, s2 = pair
        adj_list[s1.id].add(s2.id)
        adj_list[s2.id].add(s1.id)

def bfs():
    q = deque([(0, n) for n in adj_list[0]])
    visited = set()
    while q:
        src, dst = q.popleft()
        if scanners[dst].oriented:
            continue
        visited.add(dst)
        visited.add(src)

        pair = pairs.get((src, dst), None) or ScannerPair(src, dst)
        pair.collect_points_in_common()
        pair.associate_points()
        pair.find_translation()

        for n in adj_list[dst]:
            if n not in visited and not scanners[n].oriented:
                q.append((dst, n))

bfs()
beacon_set = {tuple(beacon) for scanner in scanners.values() for beacon in scanner.beacons}
print(len(beacon_set))
print(max(np.sum(np.abs(scanners[a].location - scanners[b].location)) for a, b in pairs.keys()))
