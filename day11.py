from utils.file_utils import get_lines


class Octopuss:
    def __init__(self, energy) -> None:
        self.energy = int(energy)
        self.flashed = False
        self.neighbours = set()

    def step(self):
        self.flashed = False
        self.energy += 1

    def flash(self):
        if self.energy > 9:
            self.flashed = True
            self.energy = 0
            [neighbour.flash_from_neighbour() for neighbour in self.neighbours]

    def flash_from_neighbour(self):
        if not self.flashed:
            self.energy += 1
            self.flash()


class Cavern:

    def __init__(self, lines) -> None:
        super().__init__()
        self.cavern = [[Octopuss(lines[i][j]) for i in range(len(lines[0]))] for j in range(len(lines))]
        self.add_neighbours_to_octopus()
        self.total_count = 0

    def add_neighbours_to_octopus(self):
        for i in range(len(self.cavern)):
            for j in range(len(self.cavern[0])):
                octopus = self.cavern[i][j]
                if i > 0:
                    self.add_neighbours_for_index(i - 1, j, octopus)
                self.add_neighbours_for_index(i, j, octopus)
                if i < len(self.cavern) - 1:
                    self.add_neighbours_for_index(i + 1, j, octopus)

    def add_neighbours_for_index(self, index, j, octopus):
        if j > 0:
            octopus.neighbours.add(self.cavern[index][j - 1])
        octopus.neighbours.add(self.cavern[index][j])
        if j < len(self.cavern[0]) - 1:
            octopus.neighbours.add(self.cavern[index][j + 1])

    def step(self):
        for i in range(len(self.cavern)):
            for j in range(len(self.cavern[0])):
                self.cavern[i][j].step()

    def flash(self):
        for i in range(len(self.cavern)):
            for j in range(len(self.cavern[0])):
                self.cavern[i][j].flash()
        self.total_count += self.count_flashes()

    def count_flashes(self):
        count = 0
        for i in range(len(self.cavern)):
            for j in range(len(self.cavern[0])):
                if self.cavern[i][j].flashed:
                    count += 1
        return count

    def play_steps(self):
        for i in range(100):
            self.step()
            self.flash()

    def find_synchronization(self):
        index = 0
        while self.count_flashes() != len(self.cavern) * len(self.cavern[0]):
            self.step()
            self.flash()
            index += 1
        return index


def test_parse_input():
    lines = [
        '5483143223',
        '2745854711',
        '5264556173',
        '6141336146',
        '6357385478',
        '4167524645',
        '2176841721',
        '6882881134',
        '4846848554',
        '5283751526',
    ]
    cavern = Cavern(lines)
    cavern.play_steps()
    assert cavern.total_count == 1656


def test_parse_input_part_2():
    lines = [
        '5483143223',
        '2745854711',
        '5264556173',
        '6141336146',
        '6357385478',
        '4167524645',
        '2176841721',
        '6882881134',
        '4846848554',
        '5283751526',
    ]
    cavern = Cavern(lines)
    assert cavern.find_synchronization() == 195


def test_parse_real_input():
    lines = get_lines('day11.txt')
    cavern = Cavern(lines)
    cavern.play_steps()
    assert cavern.total_count == 1656


def test_parse_real_input_2():
    lines = get_lines('day11.txt')
    cavern = Cavern(lines)
    cavern = Cavern(lines)
    assert cavern.find_synchronization() == 242
