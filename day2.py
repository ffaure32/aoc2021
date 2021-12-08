from utils.file_utils import get_lines


def compute_part1(input_list):
    horizontal_position = 0
    depth = 0
    for command in input_list:
        direction, strength = command.split()
        if direction == 'down':
            depth += int(strength)
        elif direction == 'up':
            depth -= int(strength)
        elif direction == 'forward':
            horizontal_position += int(strength)
    return depth * horizontal_position


def compute_part2(input_list):
    aim = 0
    horizontal_position = 0
    depth = 0
    for command in input_list:
        direction, strength = command.split()
        if direction == 'down':
            aim += int(strength)
        elif direction == 'up':
            aim -= int(strength)
        elif direction == 'forward':
            horizontal_position += int(strength)
            depth += (aim * int(strength))
    return depth * horizontal_position


def test_sample():
    input_list = ['forward 5', 'down 5',
                  'forward 8',
                  'up 3',
                  'down 8',
                  'forward 2']

    assert 150 == compute_part1(input_list)


def test_input():
    input_list = get_lines("day2.txt")
    assert 1561344 == compute_part1(input_list)


def test_sample_2():
    input_list = ['forward 5', 'down 5',
                  'forward 8',
                  'up 3',
                  'down 8',
                  'forward 2']

    assert 900 == compute_part2(input_list)


def test_input_part2():
    input_list = get_lines("day2.txt")
    assert 1848454425 == compute_part2(input_list)
