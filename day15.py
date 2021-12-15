import copy

from utils.file_utils import get_lines

sample_input = [
    '1163751742',
    '1381373672',
    '2136511328',
    '3694931569',
    '7463417111',
    '1319128137',
    '1359912421',
    '3125421639',
    '1293138521',
    '2311944581',
]

def find_min(rank):
    sorted_keys = sorted(rank, key=rank.get)
    if len(sorted_keys) > 0:
        return next(iter(sorted_keys))
    return None


def test_parse_input():
    assert Cavern(sample_input).compute_total_path() == 40


def test_real_parse_input():
    assert Cavern(get_lines('day15.txt')).compute_total_path() == 410

def test_parse_input_part2():
    assert Cavern(enlarge_input(sample_input)).compute_total_path() == 315

def test_real_parse_input_part2():
    assert Cavern(enlarge_input(get_lines('day15.txt'))).compute_total_path() == 2809


def enlarge_input(input):
    # enlarge horizontally
    new_lines = list()
    for line in input:
        output_line = line
        str_to_parse = copy.deepcopy(line)
        str_to_add = ''
        for i in range(4):
            for char in str_to_parse:
                str_to_add += next_int(char)
            output_line += str_to_add
            str_to_parse = str_to_add
            str_to_add = ''
        new_lines.append(output_line)

    # enlarge vertically
    new_new_lines = list()
    for line in new_lines:
        new_new_lines.append(line)
    for i in range(4):
        for j in range(len(new_lines)):
            line_to_add = ''
            for char in new_new_lines[j+len(new_lines)*i]:
                line_to_add += next_int(char)
            new_new_lines.append(line_to_add)
    return new_new_lines

def next_int(char):
    next_int = int(char)+1
    if next_int >9:
        next_int = 1
    return str(next_int)


class Cavern:

    def __init__(self, input) -> None:
        self.ranks = dict()
        self.risk_level = list()
        self.total_risk = list()
        self.opened = list()
        for y in range(len(input)):
            self.risk_level.append(list())
            self.total_risk.append(list())
            self.opened.append(list())
            for x in range(len(input[0])):
                self.risk_level[y].append(int(input[x][y]))
                self.total_risk[y].append(None)
                self.opened[y].append(True)

    def find_shortest_path(self, current_risk, current_point):
        self.opened[current_point[0]][current_point[1]] = False
        if (current_point[0], current_point[1]) in self.ranks:
            del self.ranks[current_point[0], current_point[1]]
        nexts = self.next_points(current_point)
        for next in nexts:
            current_total_risk = self.total_risk[next[0]][next[1]]
            risk_for_cell = self.risk_level[next[0]][next[1]]
            new_risk = current_risk + risk_for_cell
            if current_total_risk is None or current_total_risk > new_risk:
                self.total_risk[next[0]][next[1]] = new_risk
                self.ranks[(next[0], next[1])] = new_risk

    def compute_total_path(self):
        self.opened[0][0] = False
        starting_point = (0, 0)
        end_point = (self.max_x(), self.max_y())
        self.find_shortest_path(0, starting_point)
        while (True):
            next_value = find_min(self.ranks)
            if next_value and next_value != end_point:
                self.find_shortest_path(self.total_risk[next_value[0]][next_value[1]], next_value)
            else:
                return self.total_risk[end_point[0]][end_point[1]]


    def next_points(self, current_point):
        next_points = set()
        col = current_point[0]
        row = current_point[1]
        if row > 0 and self.opened[col][row - 1]:
            next_points.add((col, row - 1))
        if row < self.max_y() and self.opened[col][row + 1]:
            next_points.add((col, row + 1))
        if col > 0 and self.opened[col - 1][row]:
            next_points.add((col - 1, row))
        if col < self.max_x() and self.opened[col + 1][row]:
            next_points.add((col + 1, row))
        return next_points

    def max_x(self):
        return len(self.risk_level[0])-1

    def max_y(self):
        return len(self.risk_level)-1