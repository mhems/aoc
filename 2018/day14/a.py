from sys import argv

def score(n: int, seq: str) -> (str, int):
    scores = '37'
    posA, posB = 0, 1
    amount = -len(seq) - 1
    index = None
    made_enough = False
    while True:
        currentA, currentB = int(scores[posA]), int(scores[posB])
        scores += str(currentA + currentB)
        L = len(scores)
        posA = (posA + 1 + currentA) % L
        posB = (posB + 1 + currentB) % L
        #print(' '.join(scores))

        if not made_enough and len(scores) > n + 10:
            made_enough = True
        if seq in scores[amount:]:
            index = scores.index(seq)
        if index is not None and made_enough:
            print()
            break

        if L % 10_000_000 == 0:
            print(flush=True)
        elif L % 100_000 == 0:
            print('.', end='', flush=True)
    return scores[n:n+10], index

print(score(int(argv[1]), argv[1]))
