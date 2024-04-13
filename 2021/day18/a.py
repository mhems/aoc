from sys import argv
from math import ceil
from functools import reduce as fold
from itertools import permutations

class Snailfish:
    def __init__(self, left, right, value=None):
        self.left = left
        self.right = right
        self.value = value
    def magnitude(self) -> int:
        if self.value is not None:
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()
    def __str__(self) -> str:
        if self.value is not None:
            return str(self.value)
        return '[{},{}]'.format(str(self.left), str(self.right))

def construct(lists) -> Snailfish:
    if isinstance(lists[0], int):
        left = Snailfish(None, None, lists[0])
    else:
        left = construct(lists[0])
    if isinstance(lists[1], int):
        right = Snailfish(None, None, lists[1])
    else:
        right = construct(lists[1])
    return Snailfish(left, right)

def add(n1: str, n2: str) -> str:
    return reduce('[{},{}]'.format(n1, n2))

def needs_exploding(text: str) -> int:
    n = 0
    for i, l in enumerate(text):
        if l == '[':
            n += 1
            if n > 4:
                return i
        elif l == ']':
            n -= 1
    return None

def needs_splitting(text: str) -> int:
    for i, l in enumerate(text):
        if l.isdigit() and text[i+1].isdigit():
            return i-1
    return None

def reduce(text: str) -> str:
    while True:
        if i := needs_exploding(text):
            start = i
            end = text.index(']', start + 1)
            left_num, right_num = eval(text[i: end + 1])
            index_of_num_left = None
            while i > 0:
                if text[i].isdigit():
                    left_num_end = i
                    i -= 1
                    while text[i].isdigit():
                        i -= 1
                    index_of_num_left = i + 1
                    break
                i -= 1
            if index_of_num_left:
                num = int(text[index_of_num_left: left_num_end + 1]) + left_num
                left = text[:index_of_num_left] + str(num) + text[left_num_end + 1: start]
            else:
                left = text[:start]
            index_of_num_right = None
            i = end + 1
            while i < len(text):
                if text[i].isdigit():
                    index_of_num_right = i
                    i += 1
                    while text[i].isdigit():
                        i += 1
                    right_num_end = i - 1
                    break
                i += 1
            if index_of_num_right:
                num = int(text[index_of_num_right: right_num_end + 1]) + right_num
                right = text[end + 1: index_of_num_right] + str(num) + text[right_num_end + 1:]
            else:
                right = text[end + 1:]
            text = left + '0' + right
        elif i := needs_splitting(text):
            comma_index = text.find(',', i + 1)
            bracket_index = text.find(']', i + 1)
            if comma_index >= 0 and bracket_index >= 0:
                index = min(comma_index, bracket_index)
            else:
                index = max(comma_index, bracket_index)
            num = int(text[i + 1: index])
            extra = '[{},{}]'.format(num//2, ceil(num/2))
            text = text[:i+1] + extra + text[index:]
        else:
            break
    return text

def sum_magnitude(lists: [str]) -> int:
    result = fold(add, lists)
    num = construct(eval(result))
    return num.magnitude()

def biggest_sum_magnitude(lists: [str]) -> int:
    return max(sum_magnitude(permutation) for permutation in permutations(lists, 2))

lists = [line.strip() for line in open(argv[1]).readlines()]
print(sum_magnitude(lists))
print(biggest_sum_magnitude(lists))
