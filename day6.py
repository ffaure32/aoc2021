from utils.file_utils import get_lines


def new_generation(lanternfishes):
    end_of_day = list()
    for lanternfish in lanternfishes:
        if lanternfish == 0:
            lanternfish = 7
            lanternfishes.append(9)
        end_of_day.append(lanternfish - 1)
    return end_of_day


def test_standard():
    lanternfishes = list([4, 5])
    result = new_generation(lanternfishes)
    assert result == [3, 4]


def test_standard_new_bord():
    lanternfishes = list([4, 5, 0])
    result = new_generation(lanternfishes)
    assert result == [3, 4, 6, 8]


def test_sample():
    lanternfishes = [3, 4, 3, 1, 2]
    for i in range(80):
        lanternfishes = new_generation(lanternfishes)
    assert len(lanternfishes) == 5934


def test_input():
    lines = get_lines('day6.txt')
    lanternfishes = [int(age) for age in lines[0].split(',')]
    for i in range(256):
        lanternfishes = new_generation(lanternfishes)
    assert len(lanternfishes) == 5934


def test_input():
    lines = get_lines('day6.txt')
    lanternfishes = [int(age) for age in lines[0].split(',')]
    for i in range(80):
        lanternfishes = new_generation(lanternfishes)
    assert len(lanternfishes) == 352195


def test_input_dict():
    lines = get_lines('day6.txt')
    lanternfishes = [int(age) for age in lines[0].split(',')]
    dict_lanternfishes = list_to_dict(lanternfishes)
    dict_lanternfishes[0] = 0
    dict_lanternfishes[6] = 0
    dict_lanternfishes[7] = 0
    dict_lanternfishes[8] = 0
    for i in range(256):
        dict_lanternfishes = dict_generations(dict_lanternfishes)
    assert sum(dict_lanternfishes.values()) == 1600306001288


def test_sample_dict():
    lanternfishes = {0: 0, 5: 0, 6: 0, 7: 0, 8: 0, 3: 2, 4: 1, 1: 1, 2: 1}
    for i in range(256):
        lanternfishes = dict_generations(lanternfishes)
    assert sum(lanternfishes.values()) == 26984457539


def dict_generations(input_dict):
    new_dict = dict()
    new_dict[0] = input_dict[1]
    new_dict[1] = input_dict[2]
    new_dict[2] = input_dict[3]
    new_dict[3] = input_dict[4]
    new_dict[4] = input_dict[5]
    new_dict[5] = input_dict[6]
    new_dict[6] = input_dict[0] + input_dict[7]
    new_dict[7] = input_dict[8]
    new_dict[8] = input_dict[0]
    return new_dict


def list_to_dict(l):
    return dict((x, l.count(x)) for x in set(l))
