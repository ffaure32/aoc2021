from utils.file_utils import get_lines

sample_input = ['0,9 -> 5,9',
                '8,0 -> 0,8',
                '9,4 -> 3,4',
                '2,2 -> 2,1',
                '7,0 -> 7,4',
                '6,4 -> 2,0',
                '0,9 -> 2,9',
                '3,4 -> 1,4',
                '0,0 -> 8,8',
                '5,5 -> 8,2']


def test_sample():
    assert 5 == parse_input(sample_input)


def test_sample_part_2():
    assert 12 == parse_input(sample_input, True)


def test_part1():
    lines = get_lines("day5.txt")
    assert 5092 == parse_input(lines)


def test_part2():
    lines = get_lines("day5.txt")
    assert 20484 == parse_input(lines, True)


def parse_input(lines, part_2=False):
    positions = dict()
    for line in lines:
        segment = Segment(line)
        for position in segment.line(part_2):
            if position not in positions:
                positions[position] = 1
            else:
                positions[position] = positions[position] + 1

    return len([value for value in positions.values() if value >= 2])


class Segment:
    x1 = int
    y1 = int
    x2 = int
    y2 = int

    def __init__(self, line):
        segment_points = line.split(' -> ')
        first = segment_points[0].split(',')
        self.x1 = int(first[0])
        self.y1 = int(first[1])
        second = segment_points[1].split(',')
        self.x2 = int(second[0])
        self.y2 = int(second[1])

    def vertical(self):
        return self.x1 == self.x2

    def horizontal(self):
        return self.y1 == self.y2

    def diagonal(self):
        return abs(self.y1 - self.y2) == abs(self.x1 - self.x2)

    def line(self, part_2=False):
        points = set()
        if self.vertical():
            for y in range(self.min_y(), self.max_y() + 1):
                points.add((self.x1, y))
        elif self.horizontal():
            for x in range(self.min_x(), self.max_x() + 1):
                points.add((x, self.y1))
        elif self.diagonal() and part_2:
            range_x = range(abs(self.x1 - self.x2) + 1)
            for x in range_x:
                if self.x1 < self.x2:
                    if self.y1 < self.y2:
                        points.add((self.x1 + x, self.y1 + x))
                    else:
                        points.add((self.x1 + x, self.y1 - x))
                else:
                    if self.y1 < self.y2:
                        points.add((self.x1 - x, self.y1 + x))
                    else:
                        points.add((self.x1 - x, self.y1 - x))
        return points

    def min_x(self):
        return min(self.x1, self.x2)

    def max_x(self):
        return max(self.x1, self.x2)

    def min_y(self):
        return min(self.y1, self.y2)

    def max_y(self):
        return max(self.y1, self.y2)
