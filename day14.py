import collections
import copy

from utils.file_utils import get_lines

sample_lines = [
    'CH -> B',
    'HH -> N',
    'CB -> H',
    'NH -> C',
    'HB -> C',
    'HC -> B',
    'HN -> C',
    'NN -> C',
    'BH -> H',
    'NC -> B',
    'NB -> B',
    'BN -> B',
    'BB -> N',
    'BC -> B',
    'CC -> N',
    'CN -> C'
]

sample_template = 'NNCB'

#### Brut force solution for part 1
def init_pair_insertion_rules(lines):
    result = dict()
    for line in lines:
        split = line.split(' -> ')
        key = split[0]
        result[key] = key[:1] + split[1]
    return result


def apply_step(template, init_rules):
    new_template = ''
    for i in range(len(template) - 1):
        new_template += init_rules[template[i:i + 2]]
    new_template += template[-1:]
    return new_template


def test_sample_step1():
    init_rules = init_pair_insertion_rules(sample_lines)
    result = apply_step(sample_template, init_rules)
    assert result == 'NCNBCHB'


def test_sample_step2():
    init_rules = init_pair_insertion_rules(sample_lines)
    result = apply_step(sample_template, init_rules)
    result = apply_step(result, init_rules)
    assert result == 'NBCCNBBBCBHCB'


def test_sample_step10():
    init_rules = init_pair_insertion_rules(sample_lines)
    result = compute_polymer(sample_template, init_rules, 10)
    diff_max_min = get_diff_max_min(result)
    assert diff_max_min == 1588


def test_real_step10():
    init_rules = init_pair_insertion_rules(get_lines('day14.txt'))
    result = compute_polymer('CHBBKPHCPHPOKNSNCOVB', init_rules, 10)
    diff_max_min = get_diff_max_min(result)
    assert diff_max_min == 3118


def test_sample_step40():
    init_rules = init_pair_insertion_rules(sample_lines)
    result = compute_polymer(sample_template, init_rules, 40)
    diff_max_min = get_diff_max_min(result)
    assert diff_max_min == 2188189693529


def test_real_step40_part2():
    init_rules = init_pair_insertion_rules(get_lines('day14.txt'))
    result = compute_polymer('CHBBKPHCPHPOKNSNCOVB', init_rules, 40)
    diff_max_min = get_diff_max_min(result)
    assert diff_max_min == 2188189693529


def get_diff_max_min(result):
    count = collections.Counter(result)
    counts = count.values()
    diff_max_min = max(counts) - min(counts)
    return diff_max_min


def compute_polymer(template, init_rules, steps):
    result = template
    for i in range(steps):
        result = apply_step(result, init_rules)
        print(get_diff_max_min(result))
    return result


#### elegant solution for part 2
def test_sample_step10_part2():
    rules = dict()
    for line in sample_lines:
        rule = Rule(line)
        rules[rule.key] = rule

    polymer = Polymer(sample_template, rules)

    for i in range(10):
        polymer.step()
    assert polymer.count() == 1588


def test_real_step10_part2():
    rules = dict()
    for line in get_lines('day14.txt'):
        rule = Rule(line)
        rules[rule.key] = rule

    polymer = Polymer('CHBBKPHCPHPOKNSNCOVB', rules)

    for i in range(10):
        polymer.step()
    assert polymer.count() == 3118


def test_sample_step40_part2():
    rules = dict()
    for line in sample_lines:
        rule = Rule(line)
        rules[rule.key] = rule

    polymer = Polymer(sample_template, rules)

    for i in range(40):
        polymer.step()
    assert polymer.count() == 2188189693529


def test_real_step40_part2():
    rules = dict()
    for line in get_lines('day14.txt'):
        rule = Rule(line)
        rules[rule.key] = rule

    polymer = Polymer('CHBBKPHCPHPOKNSNCOVB', rules)

    for i in range(40):
        polymer.step()
    assert polymer.count() == 4332887448171

class Polymer:
    def __init__(self, template, init_rules) -> None:
        self.init_rules = init_rules
        self.insertion_rules_count = dict()
        self.letter_count = collections.Counter(template)
        for init_rule in init_rules.keys():
            self.insertion_rules_count[init_rule] = 0
        for i in range(len(template) - 1):
            rule = template[i:i + 2]
            self.insertion_rules_count[rule] += 1

    def step(self):
        new_rules_count = copy.deepcopy(self.insertion_rules_count)
        for rule in self.insertion_rules_count.keys():
            value = self.insertion_rules_count[rule]
            if value > 0:
                rule = self.init_rules[rule]
                new_rules_count[rule.values[0]] += value
                new_rules_count[rule.values[1]] += value
                new_rules_count[rule.key] -= value
                self.letter_count[rule.new_letter] += value
        self.insertion_rules_count = new_rules_count

    def count(self):
        return max(self.letter_count.values()) - min(self.letter_count.values())


class Rule:
    def __init__(self, line) -> None:
        split = line.split(' -> ')
        self.key = split[0]
        self.new_letter = split[1]
        self.values = [self.key[:1] + self.new_letter, self.new_letter + self.key[1:]]
