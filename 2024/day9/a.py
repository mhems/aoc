from sys import argv
from collections import namedtuple as nt

Block = nt('Block', ['isFile', 'size', 'id'])

def expand_single(disk: [int]) -> list:
    id = 0
    drive = []
    for i, file in enumerate(disk):
        if i % 2 == 0:
            for _ in range(file):
                drive.append(id)
            id += 1
        else:
            for _ in range(file):
                drive.append(None)
    return drive

def defrag_single(drive: [int|None]) -> [int]:
    defraged = list(drive)
    for i in range(len(defraged)):
        if i >= len(defraged):
            break
        if defraged[i] is None:
            defraged[i] = defraged.pop()
            while defraged[-1] is None:
                defraged.pop()
    return defraged

def expand_block(disk: [int]) -> [Block]:
    id = 0
    drive = []
    for i, size in enumerate(disk):
        if i % 2 == 0:
            drive.append(Block(True, size, id))
            id += 1
        else:
            drive.append(Block(False, size, None))
    return drive

def explode(drive: [Block]) -> [int|None]:
    disk = []
    for block in drive:
        if block.isFile:
            disk.extend([block.id] * block.size)
        else:
            disk.extend([None] * block.size)
    return disk

def defrag_block(drive: [Block]) -> [int]:
    for block in reversed([block for block in drive if block.isFile]):
        for i, vacancy in enumerate(drive):
            if vacancy.id == block.id:
                break
            if not vacancy.isFile:
                if block.size <= vacancy.size:
                    drive[drive.index(block)] = Block(False, block.size, None)
                    extra = vacancy.size - block.size
                    drive[i] = block
                    if extra:
                        drive.insert(i + 1, Block(False, extra, None))
                    break
    return explode(drive)

def checksum(drive: [int]) -> int:
    return sum(idx * e for idx, e in enumerate(drive) if e)

disk = list(map(int, open(argv[1]).read().strip()))
print(checksum(defrag_single(expand_single(disk))))
print(checksum(defrag_block(expand_block(disk))))
