from sys import argv
from tqdm import tqdm

class LinkedList:
    class LinkedListNode:
        def __init__(self, value):
            self.value = value
        def __iter__(node):
            start = node.value
            cur = node
            while True:
                yield cur.value
                cur = cur.next
                if cur.value == start:
                    break
    
    def __init__(self, iterable):
        contents = list(iterable)
        N = len(contents)
        node_list = [LinkedList.LinkedListNode(value) for value in contents]
        for i, node in enumerate(node_list):
            node.prev = node_list[(i-1) % N]
            node.next = node_list[(i+1) % N]
        self.head = node_list[0]
        self.lookup = {node.value: node for node in node_list}
    def __iter__(self):
        yield from self.head

def play(labels, n: int = 100):
    N = max(labels)
    wrapping_decrement = lambda x: x-1 if x > 1 else N
    labels = LinkedList(labels)    
    cur = labels.head
    for _ in tqdm(range(n)):
        a = cur.next
        b = a.next
        c = b.next
        d = c.next

        dest_value = wrapping_decrement(cur.value)
        while dest_value in (a.value, b.value, c.value):
            dest_value = wrapping_decrement(dest_value)
        
        cur.next = d
        d.prev = cur
        
        dest = labels.lookup[dest_value]
        tmp = dest.next
        dest.next = a
        a.prev = dest
        
        c.next = tmp
        tmp.prev = c

        cur = cur.next
    return labels.lookup[1]

labeling = list(int(n) for n in open(argv[1]).read().strip())
print(''.join(map(str, play(labeling)))[1:])

labeling.extend(range(max(labeling) + 1, 1_000_001))
one = play(labeling, 10_000_000)
print(one.next.value * one.next.next.value)
