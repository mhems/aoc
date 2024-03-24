from sys import argv
import heapq
from functools import reduce

class AdjustableMinHeap():
    def __init__(self):
        self.q = []
        self.entry_finder = {}

    def push(self, data, priority):
        if data in self.entry_finder:
            self.remove(data)
        entry = [priority, data, False]
        self.entry_finder[data] = entry
        heapq.heappush(self.q, entry)
        
    def remove(self, data):
        entry = self.entry_finder.pop(data)
        entry[-1] = True
    
    def pop(self):
        while self.q:
            _, data, removed = heapq.heappop(self.q)
            if not removed:
                del self.entry_finder[data]
                return data
        raise KeyError()

    def len(self):
        return len(self.present_items)

    def __contains__(self, element):
        return element in self._present_items()
    
    def _present_items(self):
        return (data for _, data, removed in self.q if not removed)

def neighbors(grid: [[int]], pos: (int, int)) -> [int]:
    ps = [tuple(a + b for a, b in zip(pos, delta))
          for delta in ((0, -1), (0, 1), (1, 0), (-1, 0))]
    return [p for p in ps
            if 0 <= p[0] < len(grid) and 0 <= p[1] < len(grid[0])]

def djikstra(grid: [[int]]) -> int:
    dist = {}
    heap = AdjustableMinHeap()
    heap.push((0, 0), 0)
    for y, row in enumerate(grid):
        for x in range(len(row)):
            dist[(y, x)] = 1e6
            heap.push((y, x), 1e6)
    dist[(0, 0)] = 0
    while heap:
        u = heap.pop()
        if u == (len(grid) - 1, len(grid[0]) - 1):
            return dist[u]
        for n in neighbors(grid, u):
            alt = dist[u] + grid[n[0]][n[1]]
            if alt < dist[n]:
                dist[n] = alt
                heap.push(n, alt)

def make_giant_grid(tile: [[int]], n: int = 5) -> [[int]]:
    tiles = [[None] * n for _ in range(n)]
    tiles[0][0] = tile
    def increment(cell: int, distance: int) -> int:
        cell += distance
        if cell > 9:
            cell = (cell % 10) + 1
        return cell
    for r in range(n):
        for c in range(n):
            if r == 0 and c == 0:
                continue
            tiles[r][c] = [[increment(cell, r + c) for cell in row] for row in tile]
    def stitch(lists) -> [int]:
        return reduce(lambda l1, l2: l1 + l2, lists)
    new_grid = []
    for row in tiles:
        for inner_y in range(len(row[0])):
            new_grid.append(stitch(row[i][inner_y] for i in range(n)))
    return new_grid

grid = [list(map(int, line.strip())) for line in open(argv[1]).readlines()]
print(djikstra(grid))
print(djikstra(make_giant_grid(grid)))
