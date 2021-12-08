from utils.file_utils import get_lines


def sum_first_digit(input_list):
    nb_elements = len(input_list)
    nb_1 = sum([int(line[0]) for line in input_list])
    if nb_1 > nb_elements / 2:
        return 1
    else:
        return 0


def sum_digit(input_list, digit_index):
    nb_elements = len(input_list)
    nb_1 = sum([int(line[digit_index]) for line in input_list])
    if nb_1 >= nb_elements / 2:
        return 1
    else:
        return 0


def test_sum_first_digit_1():
    input = ['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010', '01010']
    result = sum_digit(input, 0)
    assert 1 == result


def test_sum_first_digit_2():
    input = ['11110', '10110', '10111', '10101', '11100', '10000', '11001']
    result = sum_digit(input, 1)
    assert 0 == result


def test_filter_all():
    input = ['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010', '01010']
    nb_digits = len(input[0])
    for i in range(nb_digits):
        filter = sum_digit(input, i)
        input = [line for line in input if int(line[i]) != filter]
        print(input)


# 011101011011
# 111000100111

def test_filter_all_real():
    input = get_lines("day3.txt")
    nb_digits = len(input[0])
    for i in range(nb_digits):
        filter = sum_digit(input, i)
        input = [line for line in input if int(line[i]) != filter]
        print(input)


def compute_part2(input_list):
    sum([line[0] for line in input_list])
    for line in input_list:
        pass


def test_sample():
    binar = bin_to_dec('10110')
    invert = bin_to_dec('01001')

    assert 198 == binar * invert


def test_input():
    gamma_rate = bin_to_dec('001100100010')
    epsilon_rate = bin_to_dec('110011011101')

    assert 2640986 == gamma_rate * epsilon_rate


def test_input_2():
    oxygen_generator_rate = bin_to_dec('011101011011')
    scrubber_rate = bin_to_dec('111000100111')

    assert 6822109 == oxygen_generator_rate * scrubber_rate


def bin_to_dec(bin_str):
    return int(bin_str, 2)
