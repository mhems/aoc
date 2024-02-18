from sys import argv

def make_layers(image: str, width: int, height: int) -> [[str]]:
    layer_size = width * height
    layers = []
    for i in range(0, len(image), layer_size):
        layer = []
        for j in range(0, layer_size, width):
            layer.append(image[i + j: i + j + width])
        layers.append(layer)
    return layers

def part1(layers: [[str]]) -> int:
    layer = ''.join(min(layers, key=lambda layer: ''.join(layer).count('0')))
    return layer.count('1') * layer.count('2')   

def decode(layers: [[str]], width: int, height: int):
    result = [[None] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            n = 0
            while layers[n][y][x] == '2':
                n += 1
            result[y][x] = layers[n][y][x]
    for row in result:
        for cell in row:
            if cell != '0':
                print('#', end='')
            else:
                print(' ', end='')
        print()

image = open(argv[1]).read().strip()
width = int(argv[2])
height = int(argv[3])

layers = make_layers(image, width, height)
print(part1(layers))
decode(layers, width, height)