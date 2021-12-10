from utils.file_utils import get_lines


def remove_closest_chunks(line):
    removes = True
    while removes:
        original_len = len(line)
        line = line.replace('{}', '')
        line = line.replace('()', '')
        line = line.replace('[]', '')
        line = line.replace('<>', '')
        removes = len(line) != original_len
    return line


closing_chars = {')': 3, ']': 57, '}': 1197, '>': 25137}
opening_chars = {'(': 1, '[': 2, '{': 3, '<': 4}
closing_chars_list = list(closing_chars.keys())
valid_line = [-1, -1, -1, -1]


def clean_lines(lines):
    cleaned_lines = [remove_closest_chunks(line) for line in lines]
    result = 0
    for cleaned_line in cleaned_lines:
        indexes = [cleaned_line.find(closing_char) for closing_char in closing_chars_list]
        if indexes != valid_line:
            index = index_of_min_value(indexes)
            result += closing_chars[closing_chars_list[index]]
    return result


def index_of_min_value(indexes):
    max_i = max(indexes)
    indexes = [max_i + 1 if index == -1 and max_i != -1 else index for index in indexes]
    return indexes.index(min(indexes))


def clean_lines_part2(lines):
    cleaned_lines = [remove_closest_chunks(line) for line in lines]
    results = set()
    for cleaned_line in cleaned_lines:
        indexes = [cleaned_line.find(closing_char) for closing_char in closing_chars_list]
        if indexes == valid_line:
            results.add(compute_completion_string_score(cleaned_line))
    index = int(len(results) / 2)
    return sorted(results)[index]


def compute_completion_string_score(cleaned_line):
    total = 0
    for char in reversed(cleaned_line):
        total = total * 5 + opening_chars[char]
    return total


def test_sample():
    lines = ['[({(<(())[]>[[{[]{<()<>>',
             '[(()[<>])]({[<{<<[]>>(',
             '{([(<{}[<>[]}>{[]{[(<()>',
             '(((({<>}<{<{<>}{[]{[]{}',
             '[[<[([]))<([[{}[[()]]]',
             '[{[{({}]{}}([{[{{{}}([]',
             '{<[[]]>}<{[{[{[]{()[[[]',
             '[<(<(<(<{}))><([]([]()',
             '<{([([[(<>()){}]>(<<{{',
             '<{([{{}}[<[[[<>{}]]]>[]]']
    assert clean_lines_part2(lines) == 288957
    assert (clean_lines(lines)) == 26397


def test_input():
    lines = get_lines('day10.txt')
    assert (clean_lines(lines)) == 315693
    assert clean_lines_part2(lines) == 1870887234
