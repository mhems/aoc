from sys import argv 

class Game:
    def __init__(self, log: str):
        self.id_, self.trials = Game.parse(log)
        
    def parse(log: str) -> (int, [{str:int}]):
        left, right = log.split(':')
        left = left.lower().strip().lstrip('game')
        def parse_trial(trial_log: str) -> {str:int}:
            trial = {'r':0, 'g':0, 'b':0}
            cubes = trial_log.split(',')
            for cube in cubes:
                cube = cube.strip().lower()
                qty, color = cube.split()[:2]
                qty = int(qty)
                color = color.lower()
                if color == 'green':
                    trial['g'] += qty
                elif color == 'red':
                    trial['r'] += qty
                elif color == 'blue':
                    trial['b'] += qty
            return trial
        return int(left), list(map(parse_trial, right.split(';')))
    
    def is_feasible(self, r: int, g: int, b: int) -> bool:
        for trial in self.trials:
            if trial['r'] > r or trial['b'] > b or trial['g'] > g:
                return False
        return True
    
    def power(self):
        r = max(trial['r'] for trial in self.trials)
        g = max(trial['g'] for trial in self.trials)
        b = max(trial['b'] for trial in self.trials)
        return r * g * b
    
with open(argv[1]) as fp:
    lines = fp.readlines()
    
answer1 = sum(game.id_ for game in map(Game, lines) if game.is_feasible(12, 13, 14))
print(answer1)

answer2 = sum(game.power() for game in map(Game, lines))
print(answer2)