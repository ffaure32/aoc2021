from utils.file_utils import get_lines


def test_input():
    lines = get_lines('day8.txt')
    assert sum([(Line(line)).count_easy_digits() for line in lines]) == 321


def test_input_2():
    lines = get_lines('day8.txt')
    assert sum([(Line(line)).generate_number() for line in lines]) == 1028926


class Line:
    digits = None
    display: list

    def __init__(self, line):
        pipe = line.split(' | ')
        digits_charsets = [set(digit) for digit in pipe[0].split(' ')]
        self.digits = init_digits(digits_charsets)
        display_str = pipe[1]
        self.display = display_str.split(' ')

    def generate_number(self):
        result = ''
        for digit in self.display:
            set_digit = set(digit)
            for i in range(10):
                if set_digit == self.digits[i]:
                    result += str(i)
                    break
        return int(result)

    def count_easy_digits(self):
        count = 0
        for digit in self.display:
            length = len(digit)
            if length <= 4 or length >= 7:
                count += 1
        return count


def init_digits(digits_charsets):
    digits = [str] * 10
    digits[1] = find_unique_digit(digits_charsets, 2)
    digits[4] = find_unique_digit(digits_charsets, 4)
    digits[7] = find_unique_digit(digits_charsets, 3)
    digits[8] = find_unique_digit(digits_charsets, 7)
    five_segments_digits = find_digits(digits_charsets, 5)
    six_segments_digits = find_digits(digits_charsets, 6)

    digits[6] = find_by_common_segments(six_segments_digits, digits[1], 1)
    digits[3] = find_by_common_segments(five_segments_digits, digits[7], 3)
    digits[5] = find_by_common_segments(five_segments_digits, digits[4], 3)
    digits[2] = find_last_digit(five_segments_digits)
    digits[9] = find_by_common_segments(six_segments_digits, digits[3], 5)
    digits[0] = find_last_digit(six_segments_digits)
    return digits


def find_last_digit(set_of_segments):
    result = next(iter(set_of_segments))
    set_of_segments.remove(result)
    return result


def find_by_common_segments(set_of_segments, digit_to_compare, expected_common_segments):
    found_digit = \
        [digit for digit in set_of_segments if len(digit_to_compare.intersection(digit)) == expected_common_segments][0]
    set_of_segments.remove(found_digit)
    return found_digit


def find_unique_digit(digits_charsets, nb_chars):
    return find_digits(digits_charsets, nb_chars)[0]


def find_digits(digits_charsets, nb_chars):
    return [d_charset for d_charset in digits_charsets if len(d_charset) == nb_chars]
