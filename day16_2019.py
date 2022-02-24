from utils.file_utils import get_lines


def test_fft():
    input = '12345678'
    for i in range(4):
        input = fft(input)
    assert input == '01029498'

def test_input_1():
    input = '80871224585914546619083218645595'
    for i in range(100):
        input = fft(input)
    assert input[:8] == '24176176'


def test_real_1():
    input = get_lines('day16_2019.txt')[0]
    for i in range(100):
        input = fft(input)
    assert input[:8] == '94935919'

def test_real_1_part_2():
    input = 10000*(get_lines('day16_2019.txt')[0])
    for i in range(100):
        input = fft(input)
    assert input[:8] == '94935919'

def fft(input):
    signal = [int(c) for c in input]
    new_num = list()
    for i in range(len(signal)):
        pattern = get_pattern(i)
        digit_list = list()
        for j, num in enumerate(signal):
            digit_list.append(num * pattern[j % len(pattern)])
        new_num.append(abs(sum(digit_list)) % 10)
    return ''.join([str(x) for x in new_num])


def test_compute_pattern_real_1_part_2():
    input = 10000*(get_lines('day16_2019.txt')[0])
    build_pattern_matrix(len(input))

def build_pattern_matrix(input_length):
    all_patterns = list()
    for line in range(input_length):
        line_pattern = list()
        pattern = get_pattern(line)
        for col in range(input_length):
            line_pattern.append(pattern[col % len(pattern)])
        all_patterns.append(line_pattern)


base_pattern = [0,1,0,-1]
def get_pattern(index):
    pattern = list()
    for i in base_pattern:
        for j in range(index+1):
            pattern.append(base_pattern[i])
    pattern.append(base_pattern[0])
    del pattern[0]
    return pattern

def test_get_pattern():
    assert get_pattern(0) == [1,0,-1,0]                     #input[0]-input[2]+input[4]-input[6]
    assert get_pattern(1) == [0,1,1,0,0,-1,-1,0]            #input[1:2]-input[5:6]+input[9:10]-input[13:14]
    assert get_pattern(2) == [0,0,1,1,1,0,0,0,-1,-1,-1,0]   #input[2:4]-input[8:10]+input[14:16]-input[13:14]