from sys import argv
from collections import namedtuple as nt
from itertools import takewhile, pairwise
from functools import reduce

GEAR = -2
Tok = nt('Tok', ['val', 'loc'])
Loc = nt('Loc', ['num', 'pos', 'len'])

with open(argv[1]) as fp:
    lines = fp.readlines()

tok_list = []
for i, line in enumerate(lines):
    tok_list.append([])
    for j, ch in enumerate(line.strip()):
        if ch == '.':
            pass
        elif ch.isdigit():
            last = tok_list[i][-1] if len(tok_list[i]) > 0 else None
            if last is not None and i == last.loc.num and j < last.loc.pos + last.loc.len:
                continue
            num_str = ''.join(takewhile(lambda ch: ch.isdigit(), line[j:]))
            tok = Tok(int(num_str), Loc(i, j, len(num_str)))
            tok_list[i].append(tok)
        elif ch == '*':
            tok_list[i].append(Tok(GEAR, Loc(i, j, 1)))

def prev(a: Tok, b: Tok) -> bool:
    return a.val != GEAR and b.val == GEAR and a.loc.num == b.loc.num and a.loc.pos + a.loc.len == b.loc.pos

def next(a: Tok, b: Tok) -> bool:
    return a.val == GEAR and b.val != GEAR and a.loc.num == b.loc.num and a.loc.pos + 1 == b.loc.pos

def get_line_sum(toks: [Tok], gear: Tok) -> set:
    set_ = set()
    for num in get_nums(toks):
        if prev(num, gear) or next(gear, num):
            set_.add(num)
    return set_

def get_nums(toks: [Tok]) -> [Tok]:
    return list(tok for tok in toks if tok.val != GEAR)

def get_sum(cur_toks: [Tok], gear: Tok) -> int:
    set_ = set()
    for num in get_nums(cur_toks):
        if gear.loc.pos >= num.loc.pos - 1 and gear.loc.pos <= num.loc.pos + num.loc.len:
            set_.add(num)
    return set_

tok_list.insert(0, [])
tok_list.append([])
sum_ = 0
for key in range(1, i+2):
    cur = tok_list[key]
    for tok in cur:
        if tok.val == GEAR:
            pre = tok_list[key - 1]
            nex = tok_list[key + 1]
            set_ = get_line_sum(cur, tok)
            set_ = set_.union(get_sum(pre, tok))
            set_ = set_.union(get_sum(nex, tok))
            if len(set_) == 2:
                sum_ += reduce(lambda x, y: x.val*y.val, set_)
    
print(sum_)
