from sys import argv

class Blueprint:
    def __init__(self, id: int, ore: int, clay: int, obsidian: (int, int), geode: (int, int)):
        self.id = id
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode
        o = self.obsidian[0] + self.obsidian[1] * self.clay
        self.ore_cost_map = {
            'ore': self.ore,
            'clay': self.clay,
            'obsidian': o,
            'geode': self.geode[0] + self.obsidian[1] * o
        }
    def __str__(self) -> str:
        return str(self.id) + ': ' + str((self.ore, self.clay, self.obsidian, self.geode))
    def parse(i: int, line: str):
        tokens = line.strip().split()
        nums = [int(tokens[i]) for i in (6, 12, 18, 21, 27, 30)]
        return Blueprint(i, nums[0], nums[1], (nums[2], nums[3]), (nums[4], nums[5]))
    def max_geodes(self, time: int = 24) -> int:
        return 0
    def quality_level(self, time: int = 24) -> int:
        return self.id * self.max_geodes(time)

blueprints = [Blueprint.parse(i + 1, line.strip()) for i, line in enumerate(open(argv[1]).readlines())]
print(sum(blueprint.quality_level() for blueprint in blueprints))
