from sys import argv

class TiltTable:
    def __init__(self, text: str):
        self.width = text.index('\n')
        self.height = text.count('\n') + 1
        self.grid = [list(row) for row in text.split('\n')]
    def __str__(self) -> str:
        return '\n'.join(''.join(row) for row in self.grid)
    def load(self) -> int:
        return sum(row.count('O') * (self.height - i) for i, row in enumerate(self.grid))
    def row(self, i: int, reverse: bool = False) -> str:
        gen = self.grid[i]
        if reverse:
            gen = reversed(gen)
        return ''.join(gen)
    def col(self, i: int, reverse: bool = False) -> str:
        gen = (row[i] for row in self.grid)
        if reverse:
            gen = reversed(list(gen))
        return ''.join(gen)
    def tilt(self, dir: int = 0):
        if dir == 0 or dir == 2:
            new_cols = [self.tilt_line(self.col(x), dir == 0) for x in range(self.width)]
            self.grid = [[col[i] for col in new_cols] for i in range(self.height)]
        else:
            self.grid = [self.tilt_line(self.row(x), dir == 3) for x in range(self.height)]
    def tilt_line(self, line: str, left: bool) -> str:
        def partition(text: str) -> [str]:
            ps = []
            p = ''
            i = 0
            while i < len(text):
                if (c := text[i]) != '#':
                    p += c
                    i += 1
                else:
                    if p:
                        ps.append(p)
                    p = ''
                    while i < len(text) and (c := text[i]) == '#':
                        p += c
                        i += 1
                    ps.append(p)
                    p = ''
            if p:
                ps.append(p)
            return ps
        def roll(s: str, left: bool) -> str:
            if 'O' in s:
                func = lambda x: (x.ljust(len(s), '.') if left else x.rjust(len(s), '.'))
                return func('O' * s.count('O'))
            return s
        return ''.join(roll(e, left) for e in partition(line))
    def cycle(self, n: int = 1_000_000_000) -> int:
        seen = list()
        first_north_load = None
        for i in range(n):
            self.tilt(0)
            if first_north_load is None:
                first_north_load = self.load()
            self.tilt(3)
            self.tilt(2)
            self.tilt(1)
            s = str(self)
            if s in seen:
                start = seen.index(s)
                delta = i - start
                return first_north_load, TiltTable(seen[start + ((n - 1 - start) % delta)]).load()
            else:
                seen.append(s)
        return self.load()

with open(argv[1]) as fp:
    table = TiltTable(fp.read().strip())

print(table.cycle())
