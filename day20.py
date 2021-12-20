from utils.file_utils import get_lines


def parse_input(input):
    algorithm = input[0]
    input_image_lines = input[2:]
    return Image(algorithm, input_image_lines)


def test_parse_input():
    input = get_lines('day20_sample.txt')
    image = parse_input(input)
    image.apply_algorithm('0')
    image.apply_algorithm('0')
    assert image.count_lit_pixels() == 35


def test_parse_input_real():
    input = get_lines('day20.txt')
    image = parse_input(input)
    image.apply_algorithm('1')
    image.apply_algorithm('0')
    assert image.count_lit_pixels() == 5349


def test_parse_input_part2():
    input = get_lines('day20_sample.txt')
    image = parse_input(input)
    for i in range(50):
        image.apply_algorithm('0')
    assert image.count_lit_pixels() == 3351


def test_parse_input_real_part_2():
    input = get_lines('day20.txt')
    image = parse_input(input)
    for i in range(25):
        image.apply_algorithm('1')
        image.apply_algorithm('0')
    assert image.count_lit_pixels() == 15806


def test_binary():
    assert int('000100010', 2) == 34
    assert int('111111111', 2) == 511


class Image:
    def __init__(self, algorithm, input_image_lines) -> None:
        self.algorithm = algorithm.replace('.', '0').replace('#', '1')
        self.input_image = list()
        for line in input_image_lines:
            line = line.replace('.', '0')
            line = line.replace('#', '1')
            self.input_image.append(line)
        self.wrap_with_char_twice('0')

    def apply_algorithm(self, replacement):
        new_input = list()
        for line_index in range(1, len(self.input_image) - 1):
            new_line = ''
            for char_index in range(1, len(self.input_image[0]) - 1):
                first_line = self.input_image[line_index - 1][char_index - 1:char_index + 2]
                second_line = self.input_image[line_index][char_index - 1:char_index + 2]
                third_line = self.input_image[line_index + 1][char_index - 1:char_index + 2]
                bin_string = first_line + second_line + third_line
                new_line += self.algorithm[int(bin_string, 2)]
            new_input.append(new_line)
        self.input_image = new_input
        self.wrap_with_char_twice(replacement)

    def wrap_with_char_twice(self, char):
        self.increase_with_char(char)
        self.increase_with_char(char)

    def increase_with_char(self, replacement):
        new_input_image = list()
        new_input_image.append(generate_line(len(self.input_image[0]), replacement))
        new_input_image.extend(self.input_image)
        new_input_image.append(generate_line(len(self.input_image[0]), replacement))
        for line_index in range(len(new_input_image)):
            new_input_image[line_index] = replacement + str(new_input_image[line_index]) + replacement
        self.input_image = new_input_image

    def count_lit_pixels(self):
        total_count = 0
        for line in self.input_image:
            total_count += sum([int(c) for c in line])
        return total_count


def generate_line(line_length, char):
    return str(char * line_length)
