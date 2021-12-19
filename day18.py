import math
import re

from utils.file_utils import get_lines


def add_lines(line1, line2):
    return f'[{line1},{line2}]'


def test_add_too_lines():
    line1 = '[1,1]'
    line2 = '[2,2]'

    assert add_lines(line1, line2) == '[[1,1],[2,2]]'


def test_to_reduce():
    line = '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'
    assert to_reduce(line) == (4, -1)
    line = '[[[[0,7],4],[7,[[8,4],9]]],[1,1]]'
    assert to_reduce(line) == (16, -1)
    line = '[[[[0,7],4],[15,[0,13]]],[1,1]]'
    assert to_reduce(line) == (-1, 13)


def test_explode_1():
    assert reduce('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]') == '[[[[0,7],4],[7,[[8,4],9]]],[1,1]]'


def test_explode_2():
    assert reduce('[[[[0,7],4],[7,[[8,4],9]]],[1,1]]') == '[[[[0,7],4],[15,[0,13]]],[1,1]]'


def test_explode_3():
    assert reduce('[[[[[9,8],1],2],3],4]') == '[[[[0,9],2],3],4]'


def test_explode_4():
    assert reduce('[7,[6,[5,[4,[3,2]]]]]') == '[7,[6,[5,[7,0]]]]'


def test_explode_5():
    assert reduce('[[6,[5,[4,[3,2]]]],1]') == '[[6,[5,[7,0]]],3]'


def test_explode_6():
    assert reduce('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]') == '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'


def test_explode_7():
    assert reduce('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]') == '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'


def test_explode_8():
    assert reduce('[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]') == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'


def explode(line, explode_index):
    to_find = line[explode_index:]
    pair_start = min_digit(to_find)
    pair_end = to_find.find(']')
    separator = to_find.find(',')
    pair_0 = int(to_find[pair_start:separator])
    pair_1 = int(to_find[separator + 1:pair_end])
    left = line[:explode_index + pair_start - 1]
    right = line[explode_index + pair_end + 1:]
    to_add_left = find_next_number_left(left)
    if to_add_left:
        new_number = str(pair_0 + int(to_add_left))
        index = left.rfind(to_add_left)
        left = left[:index] + new_number + left[index + len(to_add_left):]
    to_right_add = find_next_number_right(right)
    if to_right_add:
        new_number = str(pair_1 + int(to_right_add))
        index = right.find(to_right_add)
        right = right[:index] + new_number + right[index + len(to_right_add):]

    return left + '0' + right


def test_find_next_number_right():
    assert find_next_number_right("toto 434 is dead 45") == "434"


def test_find_next_number_left():
    assert find_next_number_left("toto 434 is dead 45") == "45"


def find_next_number_right(input):
    numbers = re.findall('[0-9]+', input)
    if len(numbers) > 0:
        return numbers[0]


def find_next_number_left(input):
    numbers = re.findall('[0-9]+', input)
    if len(numbers) > 0:
        return numbers[-1]


def max_digit(line):
    digits = {ind: x for ind, x in enumerate(line) if x.isdigit()}
    if len(digits) > 0:
        return max(digits.keys())


def min_digit(line):
    digits = {ind: x for ind, x in enumerate(line) if x.isdigit()}
    if len(digits) > 0:
        return min(digits.keys())


def split(line, index):
    to_replace = line[index:index + 2]
    number = int(to_replace)
    divided = number / 2
    right = str(int(math.ceil(divided)))
    left = str(int(divided))
    return line.replace(to_replace, f'[{left},{right}]', 1)


def test_split_1():
    assert split('10', 0) == '[5,5]'


def test_split_2():
    assert split('11', 0) == '[5,6]'


def test_split_3():
    assert split('20', 0) == '[10,10]'


def test_split_big():
    assert split('[[[[0,7],4],[15,[0,13]]],[1,1]]', 13) == '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'


def reduce(line):
    is_to_reduce = to_reduce(line)
    if is_to_reduce:
        if is_to_reduce[0] > -1:
            return explode(line, is_to_reduce[0])
        else:
            return split(line, is_to_reduce[1])


def complete_addition(input):
    result = input[0]
    for i in range(1, len(input)):
        result = reduce_add_lines(result, input[i])
    return result


def test_sample():
    input = [
        '[1,1]',
        '[2,2]',
        '[3,3]',
        '[4,4]',
        '[5,5]'
    ]
    assert complete_addition(input) == '[[[[3,0],[5,3]],[4,4]],[5,5]]'


def test_sample_2():
    input = [
        '[1,1]',
        '[2,2]',
        '[3,3]',
        '[4,4]',
        '[5,5]',
        '[6,6]'
    ]
    assert complete_addition(input) == '[[[[5,0],[7,4]],[5,5]],[6,6]]'


def test_other_big_sample():
    input = [
        '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
        '[[[5,[2,8]],4],[5,[[9,9],0]]]',
        '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]',
        '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]',
        '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]',
        '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]',
        '[[[[5,4],[7,7]],8],[[8,3],8]]',
        '[[9,3],[[9,9],[6,[4,9]]]]',
        '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
        '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'
    ]
    assert complete_addition(input) == '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]'


def test_big_sample():
    input = [
        '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
        '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
        '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
        '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
        '[7,[5,[[3,8],[1,4]]]]',
        '[[2,[2,2]],[8,[8,1]]]',
        '[2,9]',
        '[1,[[[9,3],9],[[9,0],[0,7]]]]',
        '[[[5,[7,4]],7],1]',
        '[[[[4,2],2],6],[8,7]]',
    ]
    assert complete_addition(input) == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'


def test_sum_real_input():
    input = get_lines('day18.txt')
    addition = complete_addition(input)
    assert addition == '[[[[6,6],[6,7]],[[9,5],[8,0]]],[[[7,8],[7,8]],[9,2]]]'
    assert parse_pair_input(addition).magnitude() == 12

def test_largers_magnitude():
    input =[
        '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
        '[[[5,[2,8]],4],[5,[[9,9],0]]]',
        '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]',
        '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]',
        '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]',
        '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]',
        '[[[[5,4],[7,7]],8],[[8,3],8]]',
        '[[9,3],[[9,9],[6,[4,9]]]]',
        '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
        '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'
    ]
    assert find_largest_magnitude(input) == 3993

def test_sum_real_input():
    input = get_lines('day18.txt')
    assert find_largest_magnitude(input) == 4763

def find_largest_magnitude(lines):
    magnitudes = set()
    for line in lines:
        for other_line in lines:
            if other_line != line:
                addition = reduce_add_lines(line, other_line)
                magnitudes.add(parse_pair_input(addition).magnitude())
    return max(magnitudes)

def reduce_add_lines(line1, line2):
    line = add_lines(line1, line2)
    while (to_reduce(line)):
        line = reduce(line)
    return line


def to_reduce(line):
    opend_pairs_count = 0
    for i in range(len(line)):
        char = line[i]
        if char == '[':
            opend_pairs_count += 1
            if opend_pairs_count == 5:
                return (i, -1)
        elif char == ']':
            opend_pairs_count -= 1

    for i in range(len(line)):
        char = line[i]
        if char.isdigit():
            if line[i + 1].isdigit():
                return (-1, i)


def test_raw_pair():
    input = '[1,2]'
    pair = Pair(input)
    assert pair.left == 1
    assert pair.right == 2
    assert pair.magnitude() == 7

def test_parse_input():
    to_parse = '[3,5]'
    pair = parse_pair_input(to_parse)
    assert pair.magnitude() == 19
    assert parse_pair_input('[[9,1],[1,9]]').magnitude() == 129
    assert parse_pair_input('[[1,2],[[3,4],5]]').magnitude() == 143
    assert parse_pair_input('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]').magnitude() == 3488

def parse_pair_input(input):
    opened = 0
    for index, c in enumerate(input):
        if c == '[':
            opened +=1
        elif c== ']':
            opened -=1
        elif c == ',' and opened == 1:
            break
    left_pair = input[1:index]
    right_pair = input[index+1:-1]
    pair = Pair()
    if left_pair.find('[')>=0:
        pair.left = parse_pair_input(left_pair)
    else:
        pair.left = int(left_pair)
    if right_pair.find('[')>=0:
        pair.right = parse_pair_input(right_pair)
    else:
        pair.right = int(right_pair)
    return pair

class Pair:

    def __init__(self, input = '') -> None:
        super().__init__()
        if input.count('[') == 1:
            line = input.replace('[', '').replace(']', '')
            split = line.split(',')
            self.left = int(split[0])
            self.right = int(split[1])

    def magnitude(self):
        return self.left_mag() * 3 + self.right_mag() * 2

    def left_mag(self):
        if type(self.left) is int:
            return self.left
        else:
            return self.left.magnitude()

    def right_mag(self):
        if type(self.right) is int:
            return self.right
        else:
            return self.right.magnitude()


def test_reduce():
    line = '[[[[[9,8],1],2],3],4]'

    assert reduce(line) == '[[[[0,9],2],3],4]'
