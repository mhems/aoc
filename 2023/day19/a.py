from sys import argv
from collections import namedtuple as nt

with open(argv[1]) as fp:
    lines = fp.readlines()

Workflow = nt('Workflow', ['name', 'rules'])
Rule = nt('Rule', ['condition', 'destination'])
Part = nt('Part', ['x', 'm', 'a', 's'])

def parse_part(s: str) -> Part:
    tokens = list(map(lambda x: int(x[2:]), s.strip().strip('{}').split(',')))
    return Part(*tokens)

def parse_rule(s: str) -> Rule:
    if ':' not in s:
        return Rule(lambda _: True, s.strip())
    cond, state = s.split(':')
    def filter(part: Part) -> bool:
        return eval('part.' + cond)
    return Rule(filter, state)

def parse_workflow(s: str) -> Workflow:
    name, right = s.split('{')
    rules = list(map(parse_rule, right.strip('}').split(',')))
    return Workflow(name, rules)

workflows = {}
parts = []
parsing_parts = False
for line in lines:
    if len(line.strip()) == 0:
        parsing_parts = True
        continue
    if parsing_parts:
        parts.append(parse_part(line.strip()))
    else:
        workflow = parse_workflow(line.strip())
        workflows[workflow.name] = workflow

def process_workflow(part: Part, workflow: Workflow) -> str:
    for rule in workflow.rules:
        if rule.condition is None:
            return rule.destination
        elif rule.condition(part):
            return rule.destination
    raise Exception('no matching rules for part ' + str(part))

def is_good(part: Part, current: Workflow, workflows: {str:Workflow}) -> bool:
    output = process_workflow(part, current)
    if output == 'A':
        return True
    if output == 'R':
        return False
    return is_good(part, workflows[output], workflows)

answer = 0
for part in parts:
    if is_good(part, workflows['in'], workflows):
        answer += sum(part)
print(answer)
