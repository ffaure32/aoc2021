import numpy

from utils.file_utils import get_lines


def get_neighbours_coords(lines, num_row, num_col):
    coords = set()
    if num_row > 0:
        coords.add((num_row - 1, num_col))
    if num_row < len(lines) - 1:
        coords.add((num_row + 1, num_col))
    if num_col > 0:
        coords.add((num_row, num_col - 1))
    if num_col < len(lines[0]) - 1:
        coords.add((num_row, num_col + 1))
    return coords


class PointWithNeighbours():
    value: int
    neighbours: set

    def __init__(self, lines, num_row, num_col):
        self.neighbours = set()
        self.value = int(lines[num_row][num_col])
        for coords in get_neighbours_coords(lines, num_row, num_col):
            self.neighbours.add(int(lines[coords[0]][coords[1]]))

    def risk_level(self):
        if self.value < min(self.neighbours):
            return 1 + self.value
        else:
            return 0


def test_sample():
    lines = ['2199943210',
             '3987894921',
             '9856789892',
             '8767896789',
             '9899965678']
    assert calculate_risk_level(lines) == 15


def test_input():
    lines = get_lines('day9.txt')
    assert calculate_risk_level(lines) == 530


def calculate_risk_level(lines):
    points = set()
    for num_row in range(0, len(lines)):
        for num_col in range(0, len(lines[0])):
            points.add(PointWithNeighbours(lines, num_row, num_col))
    return sum([point.risk_level() for point in points])


def test_sample_part2():
    lines = ['2199943210',
             '3987894921',
             '9856789892',
             '8767896789',
             '9899965678']
    builder = BasinBuilder(lines)
    assert builder.find_biggest_basins() == 1134


def test_input_part2():
    lines = get_lines('day9.txt')
    builder = BasinBuilder(lines)
    assert builder.find_biggest_basins() == 1019494


def build_basin(lines, num_col, num_row):
    return Basin(lines, num_col, num_row)


class BasinBuilder:
    coords_in_basin: set
    basins: set

    def __init__(self, lines):
        self.lines = lines
        self.coords_in_basin = set()
        self.basins = set()
        for num_row in range(0, len(lines)):
            for num_col in range(0, len(lines[0])):
                new_coord = (num_col, num_row)
                value = int(lines[num_row][num_col])
                if new_coord not in self.coords_in_basin and value < 9:
                    basin = build_basin(lines, num_col, num_row)
                    self.coords_in_basin.update(basin.points_in_basin)
                    self.basins.add(basin)

    def find_biggest_basins(self):
        sorted_basins = sorted(self.basins)
        last_elements = sorted_basins[-3:]
        return numpy.prod([basin.size() for basin in last_elements])


class Basin:
    points_in_basin: set

    def __init__(self, lines, num_col, num_row):
        self.lines = lines
        self.points_in_basin = set()
        self.points_in_basin.add((num_col, num_row))
        self.add_to_basin(num_col, num_row)

    def add_to_basin(self, num_col, num_row):
        for coords in get_neighbours_coords(self.lines, num_row, num_col):
            self.add_to_basin_with_coords(coords[1], coords[0])

    def add_to_basin_with_coords(self, num_col, num_row):
        point_to_add = (num_col, num_row)
        if point_to_add not in self.points_in_basin and int(self.lines[num_row][num_col]) < 9:
            self.points_in_basin.add(point_to_add)
            self.add_to_basin(num_col, num_row)

    def size(self):
        return len(self.points_in_basin)

    def __lt__(self, other):
        return self.size() < other.size()
