amounts = sorted((sum(map(int, l.strip().split('\n'))) for l in open('input.txt').read().split('\n\n')), reverse=True)
print(amounts[0])
print(sum(amounts[:3]))
