import sys
from typing import Iterable

class Slice:
    def __init__(self, start: int, stop: int):
        self.start = start
        self.stop = stop
    def in_range(self, num: int):
        return self.start <= num <= self.stop
class SliceCollection:
    def __init__(self, slices: Iterable[tuple[int, int]]):
        sorted_slices = sorted(slices)
        self.slices = [Slice(*sorted_slices[0])]
        for start, stop in sorted_slices[1:]:
            if self.slices[-1].stop + 1 == start or self.slices[-1].start <= start <= self.slices[-1].stop:
                self.slices[-1].stop = max(stop, self.slices[-1].stop)
            else:
                self.slices.append(Slice(start, stop))
    def in_range(self, num: int, low: int = 0, high: int|None = None) -> bool:
        if high is None:
            high = len(self.slices) - 1
        if low > high:
            return False
        if high == low:
            return self.slices[low].in_range(num)
        mid = low + (high - low) // 2
        if self.slices[mid].in_range(num):
            return True
        if num < self.slices[mid].start:
            return self.in_range(num, low, mid - 1)
        return self.in_range(num, mid + 1, high)

fresh, available = open(sys.argv[1]).read().rstrip().split('\n\n')
slices = SliceCollection(tuple(map(int, slice.rstrip().split('-'))) for slice in fresh.split('\n'))
available = [int(id.rstrip()) for id in available.split('\n')]
print(sum(int(slices.in_range(item)) for item in available))
print(sum(slice.stop - slice.start + 1 for slice in slices.slices))
