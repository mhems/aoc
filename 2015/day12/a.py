from sys import argv
import re
import json

with open(argv[1]) as fp:
    lines = fp.readlines()
text = lines[0].strip()

regex = re.compile(r'-?[1-9][0-9]*')

answer = sum(int(match.group(0)) for match in re.finditer(regex, text))
print(answer)

def value(item) -> int:
    if isinstance(item, int):
        return item
    if isinstance(item, str):
        return 0
    if isinstance(item, list):
        return sum(value(e) for e in item)
    if isinstance(item, dict):
        if "red" in item.values():
            return 0
        return sum(value(k) + value(v) for k, v in item.items())
    raise ValueError()

doc = json.loads(text)
print(value(doc))
    