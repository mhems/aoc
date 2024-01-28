from sys import argv
from collections import namedtuple as nt
import re

Span = nt('Span', ['id', 'date', 'start', 'stop'])
regex = re.compile(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})')

with open(argv[1]) as fp:
    lines = fp.readlines()

def parse_schedule(lines: [str]) -> [Span]:
    def by_datetime(line: str) -> (int, int, int, int, int):
        return tuple(int(m) for m in re.search(regex, line.strip()).groups())
    lines = sorted(lines, key=by_datetime)
    spans = []
    for line in lines:
        tokens = line.strip().split()
        date = tokens[0][1:]
        minute = int(tokens[1][3:5])
        if tokens[2] == 'Guard':
            guard = int(tokens[3][1:])
        elif tokens[2] == 'falls':
            start = minute
        elif tokens[2] == 'wakes':
            stop = minute
            spans.append(Span(guard, date, start, stop))
    return spans

def strategy1(spans: [Span]) -> int:
    amount_map = {}
    mode_map = {}
    for span in spans:
        if span.id not in amount_map:
            amount_map[span.id] = 0
        amount_map[span.id] += span.stop - span.start
        if span.id not in mode_map:
            mode_map[span.id] = [0] * 60
        for minute in range(span.start, span.stop):
            mode_map[span.id][minute] += 1
    most_asleep = max(amount_map.keys(), key=lambda id: amount_map[id])
    minute_mode = max(range(60), key=lambda i: mode_map[most_asleep][i])
    return most_asleep * minute_mode

def strategy2(spans: [Span]) -> int:
    amount_map = {}
    mode_map = {}
    for span in spans:
        if span.id not in amount_map:
            amount_map[span.id] = 0
        amount_map[span.id] += span.stop - span.start
        if span.id not in mode_map:
            mode_map[span.id] = [0] * 60
        for minute in range(span.start, span.stop):
            mode_map[span.id][minute] += 1
    most_same_minute_asleep = max(mode_map.keys(), key=lambda id: max(mode_map[id]))
    minute_mode = sorted(range(60), key=lambda i: mode_map[most_same_minute_asleep][i], reverse=True)[0]
    return most_same_minute_asleep * minute_mode

spans = parse_schedule(lines)
print(strategy1(spans))
print(strategy2(spans))