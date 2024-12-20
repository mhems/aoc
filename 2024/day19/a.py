from sys import argv

def num_possible(design: str, patterns: {str}) -> int:
    cache = {pattern: 1 for pattern in patterns if len(pattern) == 1}
    def inner(design: str) -> int:
        cached = cache.get(design, None)
        if cached is not None:
            return cached
        cache[design] = sum(1 if design == pattern else inner(design[len(pattern):])
                            for pattern in patterns if design.startswith(pattern))
        return cache[design]
    return inner(design)

patterns, designs = open(argv[1]).read().split('\n\n')
patterns = frozenset(patterns.strip().split(', '))
designs = list(designs.strip().split('\n'))
nums = [num_possible(design, patterns) for design in designs]
print(sum(int(num > 0) for num in nums))
print(sum(nums))
