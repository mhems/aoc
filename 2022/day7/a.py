from sys import argv

class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.sz = size
    def size(self) -> int:
        return self.sz
    def __str__(self) -> str:
        return '{} ({})'.format(self.name, self.sz)
class Dir:
    def __init__(self, name: str):
        self.name = name
        self.contents = []
    def add(self, item):
        self.contents.append(item)
    def size(self) -> int:
        return sum(item.size() for item in self.contents)
    def dirs(self):
        def rec_dir(dir):
            yield dir
            for item in dir.contents:
                if isinstance(item, Dir):
                    yield from rec_dir(item)
        return rec_dir(self)
    def __str__(self) -> str:
        def rec_str(dir, n: int):
            s = ' ' * n + '- ' + dir.name + ' (' + str(dir.size()) + ')\n'
            for item in dir.contents:
                if isinstance(item, File):
                    s += ' ' * n + '  - ' + str(item) + '\n'
                else:
                    s += rec_str(item, n + 2)
            return s
        return rec_str(self, 0)

def create_tree(log: [str], index: int = 0) -> (Dir, int):
    root = Dir(log[index].split()[-1])
    i = index + 1
    while i < len(log):
        line = log[i]
        if line.startswith('$ ls'):
            pass
        elif line.startswith('dir'):
            pass
        elif line.startswith('$ cd'):
            if '..' in line:
                return root, i
            dir, i = create_tree(log, i)
            root.add(dir)
        else:
            tokens = line.split()
            root.add(File(tokens[1], int(tokens[0])))
        i += 1
    return root, i

def find_deletion(dir: Dir, unused: int = 30000000, total: int = 70000000) -> int:
    needed = unused - (total - dir.size())
    dir_sizes = sorted(d.size() for d in dir.dirs())
    for size in dir_sizes:
        if size >= needed:
            return size

root, _ = create_tree([line.strip() for line in open(argv[1]).readlines()])
print(sum(size for dir in root.dirs() if (size := dir.size()) <= 100000))
print(find_deletion(root))
