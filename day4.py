import numpy

from utils.file_utils import get_lines


def test_grid_init():
    input = [
        '97 18 90 62 17',
        '98 88 49 41 74',
        '66  9 83 69 91',
        '33 57  3 71 43',
        '11 50  7 10 28'
    ]
    grid = Grid(input)
    grid.draw(57)
    print(grid.lines)
    print(grid.columns)


def lines_to_matrix(lines):
    matrix = [[int(num) for num in line.split()] for line in lines]
    return numpy.matrix(matrix)


def test_part1():
    draws, grids = build_grids()

    result = execute_draws(draws, grids)

    assert 6592 == result


def test_part2():
    draws, grids = build_grids()

    result = find_last_bingo(draws, grids)

    assert 31755 == result


def execute_draws(draws, grids):
    for draw in draws:
        for grid in grids:
            bingo = grid.draw(draw)
            if bingo:
                return grid.sum_lasting_numbers() * draw
    return False


def find_last_bingo(draws, grids):
    for draw in draws:
        incomplete_grids = find_incomplete_grids(grids)
        for grid in incomplete_grids:
            bingo = grid.draw(draw)
            if bingo:
                grid.bingo = True
                if len(find_incomplete_grids(incomplete_grids)) == 0:
                    return grid.sum_lasting_numbers() * draw
    return False


def find_incomplete_grids(grids):
    return [grid for grid in grids if not grid.bingo]


def build_grids():
    input = get_lines("day4_arnaud.txt")
    draws = [int(draw) for draw in input[0].split(',')]
    index = 1
    grids = list()
    while index < len(input):
        lines = list()
        lines.append(input[index + 1])
        lines.append(input[index + 2])
        lines.append(input[index + 3])
        lines.append(input[index + 4])
        lines.append(input[index + 5])
        grids.append(Grid(lines))
        index += 6
    return draws, grids


class Grid:
    lines = set()
    columns = set()
    bingo = False

    def __init__(self, input):
        matrix = lines_to_matrix(input)
        self.lines = [set(line) for line in matrix.tolist()]
        v_matrix = matrix.T
        self.columns = [set(col) for col in v_matrix.tolist()]

    def draw(self, number):
        for line in self.lines:
            if number in line:
                line.remove(number)
                if len(line) == 0:
                    return True
        for line in self.columns:
            if number in line:
                line.remove(number)
                if len(line) == 0:
                    return True
        return False

    def sum_lasting_numbers(self):
        result = 0
        for line in self.lines:
            result += sum(line)
        return result