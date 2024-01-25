from sys import argv

class Layer:
    def __init__(self, index: int, depth: int):
        self.severity = index * depth
        self.index = index
        self.depth = depth
        self.pos = 0
        self.down = True

    def step(self):
        if self.down:
            if self.pos == self.depth - 1:
                self.down = False
                self.pos -= 1
            else:
                self.pos += 1
        else:
            if self.pos == 0:
                self.down = True
                self.pos = 1
            else:
                self.pos -= 1
                
    def reset(self):
        self.pos = 0
        self.down = True
    
    def clone(self):
        layer = Layer(self.index, self.depth)
        layer.pos = self.pos
        layer.down = self.down
        return layer

with open(argv[1]) as fp:
    lines = fp.readlines()

layers = [Layer(*map(int, line.strip().split(': '))) for line in lines]
layers = {layer.index : layer for layer in layers}

def step(layers: {int, Layer}) -> int:
    severity = 0
    for i in range(max(layers.keys()) + 1):
        if i in layers and layers[i].pos == 0:
            severity += layers[i].severity
        for layer in layers.values():
            layer.step()
    return severity

def gets_caught(layers: {int, Layer}) -> bool:
    for i in range(max(layers.keys()) + 1):
        if i in layers and layers[i].pos == 0:
            return True
        for layer in layers.values():
            layer.step()
    return False

print(step(layers))

def find_safe_delay(layers: {int, Layer}) -> int:
    i = 0
    while True:
        if not gets_caught({index: layer.clone() for index, layer in layers.items()}):
            return i
        for layer in layers.values():
            layer.step()
        if i % 100_000 == 0:
            print('.', end='', flush=True)
        i += 1

for layer in layers.values():
    layer.reset()

print(find_safe_delay(layers))
