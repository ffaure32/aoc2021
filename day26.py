from utils.file_utils import get_lines


def test_sample():
    input = [
        'v...>>.vv>',
        '.vv>>.vv..',
        '>>.>v>...v',
        '>>v>>.>.v.',
        'v>v.vv.v..',
        '>.>>..v...',
        '.vv..>.>v.',
        'v.v..>>v.v',
        '....v..v.>',
    ]
    count = count_moves(input)
    assert count == 58


def test_real_input():
    input = get_lines('day25.txt')
    count = count_moves(input)
    assert count == 601


def count_moves(input):
    map = CucumberMap(input)
    count = 1
    while (map.move()):
        count += 1
    return count


class CucumberMap:

    def __init__(self, input) -> None:
        self.east = set()
        self.south = set()
        self.x_size = len(input[0])
        self.y_size = len(input)
        for y_index, line in enumerate(input):
            for x_index, char in enumerate(line):
                if char == '>':
                    self.east.add((x_index, y_index))
                elif char == 'v':
                    self.south.add((x_index, y_index))

    def move(self):
        next_souths = set()
        next_easts = set()
        busy = self.east.union(self.south)
        for east in self.east:
            next_east = self.next_coords_east(east)
            if next_east not in busy:
                next_easts.add(next_east)
            else:
                next_easts.add(east)
        still_moving = next_easts != self.east
        self.east = next_easts

        busy = self.east.union(self.south)
        for south in self.south:
            next_south = self.next_coords_south(south)
            if next_south not in busy:
                next_souths.add(next_south)
            else:
                next_souths.add(south)
        still_moving = still_moving or next_souths != self.south
        self.south = next_souths

        return still_moving

    def next_coords_east(self, east):
        new_east = east[0]+1
        if new_east == self.x_size:
            new_east = 0
        return new_east, east[1]

    def next_coords_south(self, south):
        new_south = south[1]+1
        if new_south == self.y_size:
            new_south = 0
        return (south[0], new_south)