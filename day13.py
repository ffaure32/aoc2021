from utils.file_utils import get_lines

sample_input = [
    '6, 10',
    '0, 14',
    '9, 10',
    '0, 3',
    '10, 4',
    '4, 11',
    '6, 0',
    '6, 12',
    '4, 1',
    '0, 13',
    '10, 12',
    '3, 4',
    '3, 0',
    '8, 4',
    '1, 10',
    '2, 14',
    '8, 10',
    '9, 0',
]


def test_parse_input_first_sample():
    lines = sample_input
    y = 7
    x = 5

    paper = init_input(lines, x, y)
    result_part1 = fold_x(paper, x)

    assert sum([sum(line) for line in result_part1]) == 17


def test_parse_input_first_sample_part_2():
    lines = sample_input
    y = 7
    x = 5
    paper = init_input(lines, x, y)

    result = fold_y(paper, y)
    result = fold_x(result, x)
    print_result(result)


def test_part1_input():
    lines = get_lines('day13.txt')
    y = 447
    x = 655

    paper = init_input(lines, x, y)
    result_part1 = fold_x(paper, x)

    assert sum([sum(line) for line in result_part1]) == 847

def test_part2_input():
    lines = get_lines('day13.txt')
    y = 447
    x = 655

    paper = init_input(lines, x, y)
    result = fold_paper(paper, 655, 447)
    result = fold_paper(result, 327, 223)
    result = fold_paper(result, 163, 111)
    result = fold_paper(result, 81, 55)
    result = fold_paper(result, 40, 27)

    result = fold_y(result, 13)
    result = fold_y(result, 6)
    print_result(result)


def print_result(result):
    print()
    for line in result:
        print(''.join(['#' if x else '.' for x in line]))


def fold_paper(input, x, y):
    result = fold_x(input, x)
    result = fold_y(result, y)
    return result


def init_input(lines, x, y):
    paper = [[False for col in range(x * 2 + 1)] for row in range(y * 2 + 1)]
    for line in lines:
        coords = line.split(',')
        paper[int(coords[1].strip())][int(coords[0].strip())] = True
    return paper


def fold_x(paper, x):
    part1 = list()
    part2 = list()
    for row in range(len(paper)):
        part1.append(paper[row][:x])
        part2.append(paper[row][x + 1:][::-1])
    return merge_2_parts(part1, part2)


def fold_y(paper, y):
    part1 = paper[:y]
    part2 = paper[y + 1:][::-1]
    return merge_2_parts(part1, part2)


def merge_2_parts(part1, part2):
    result = list()
    row_length = len(part1[0])
    for row in range(len(part1)):
        line = list()
        result.append(line)
        for col in range(row_length):
            line.append(part1[row][col] or part2[row][col])
    return result
