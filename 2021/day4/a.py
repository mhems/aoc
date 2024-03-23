from sys import argv

def parse_board(text: str) -> [[int]]:
    return [[int(token) for token in line.strip().split()]
            for line in text.strip().split('\n')]

def bingo(nums: [int], boards: [[int]], lose: bool = False) -> int:
    drawn, exclude = set(), set()
    for num in nums:
        drawn.add(num)
        for i, board in enumerate(boards):
            if i not in exclude:
                for j in range(len(board)):
                    if (all(e in drawn for e in board[j]) or
                        all(e in drawn for e in (row[j] for row in board))):
                        if not lose or len(exclude) == len(boards) - 1:
                            return num * sum(sum(e for e in row if e not in drawn) for row in board)
                        exclude.add(i)

chunks = open(argv[1]).read().split('\n\n')
nums = [int(token) for token in chunks[0].strip().split(',')]
boards = [parse_board(chunk) for chunk in chunks[1:]]
print(bingo(nums, boards))
print(bingo(nums, boards, True))
