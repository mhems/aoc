from sys import argv
from collections import namedtuple as nt
from itertools import takewhile, pairwise

SYM = -1
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
        else:
            tok_list[i].append(Tok(SYM, Loc(i, j, 1)))

def contains_sym(toks: [Tok]) -> bool:
    return any(map(lambda tok: tok.val == SYM, toks))

def contains_num(toks: [Tok]) -> bool:
    return any(map(lambda tok: tok.val != SYM, toks))

def prev(a: Tok, b: Tok) -> bool:
    return a.val != SYM and b.val == SYM and a.loc.num == b.loc.num and a.loc.pos + a.loc.len == b.loc.pos

def next(a: Tok, b: Tok) -> bool:
    return a.val == SYM and b.val != SYM and a.loc.num == b.loc.num and a.loc.pos + 1 == b.loc.pos

def get_line_sum(toks: [Tok]) -> set:
    set_ = set()
    if contains_sym(toks) and contains_num(toks):
        for pair in pairwise(toks):
            if prev(*pair):
                set_.add(pair[0])
            elif next(*pair):
                set_.add(pair[1])
    return set_

def get_syms(toks: [Tok]) -> [Tok]:
    return list(tok for tok in toks if tok.val == SYM)

def get_nums(toks: [Tok]) -> [Tok]:
    return list(tok for tok in toks if tok.val != SYM)

def get_prev_sum(prev_toks: [Tok], cur_toks: [Tok]) -> int:
    set_ = set()
    for sym in get_syms(prev_toks):
        for num in get_nums(cur_toks):
            if sym.loc.pos >= num.loc.pos - 1 and sym.loc.pos <= num.loc.pos + num.loc.len:
                set_.add(num)
    return set_
            
def get_next_sum(cur_toks: [Tok], next_toks: [Tok]) -> int:
    set_ = set()
    for sym in get_syms(next_toks):
        for num in get_nums(cur_toks):
            if sym.loc.pos >= num.loc.pos - 1 and sym.loc.pos <= num.loc.pos + num.loc.len:
                set_.add(num)
    return set_

tok_list.insert(0, [])
tok_list.append([])
set_ = set()
for key in range(1, i+2):
    pre = tok_list[key - 1]
    cur = tok_list[key]
    nex = tok_list[key + 1]
    set_ = set_.union(get_line_sum(cur))
    set_ = set_.union(get_prev_sum(pre, cur))
    set_ = set_.union(get_next_sum(cur, nex))
    
answer = sum(tok.val for tok in set_)
print(answer)
