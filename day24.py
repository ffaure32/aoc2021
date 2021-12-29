import math

from utils.file_utils import get_lines


class Alu:

    def __init__(self, inputs) -> None:
        self.variables = {'x':0, 'y':0, 'z':0, 'w':0}
        self.inputs= [int(c) for c in inputs]
        self.input_index = 0


    def parse_line(self, split):
        if len(split) > 2:
            a = self.variables[split[1]]
            if str(split[2]).isalpha():
                b= self.variables[split[2]]
            else:
                b= int(split[2])
        op = split[0]
        if op == 'inp':
            self.variables[split[1]] = self.inputs[self.input_index]
            self.input_index+=1
        elif op == 'add':
            self.variables[split[1]] = a + b
        elif op == 'mul':
            self.variables[split[1]] = a * b
        elif op == 'div':
            if b != 0:
                self.variables[split[1]] = math.trunc(a / b)
        elif op == 'mod':
            if a>=0 and b>0:
                self.variables[split[1]] = math.trunc(a % b)
        else:
            self.variables[split[1]] = 1 if a == b else 0

def find_biggest_monad(lines):
    start = 99999999999999
    stop  = 11111111111111
    for i in range(start, 0, -1):
        input = str(i)
        if '0' not in input:
            alu = Alu(input)
            try:
                for line in lines:
                    alu.parse_line(line)
                if alu.variables['z'] == 0:
                    return input
            except Exception:
                continue


def compute_monad(lines, w_values):
    alu = Alu(w_values)
    try:
        for line in lines:
            alu.parse_line(line)
    except Exception:
        return None
    return alu


def test_input():
    lines = get_lines('day24.txt')
    lines = [line.split(' ') for line in lines]
    assert find_biggest_monad(lines) == '99520009949993'


def test_values():
    lines = get_lines('day24.txt')
    lines = [line.split(' ') for line in lines]
    print(compute_monad(lines, '96299896449997').variables)


def test_negate():
    lines = [
        'inp z',
        'inp x',
        'mul z 3',
        'eql z x',
    ]
    lines = [line.split(' ') for line in lines]
    print(compute_monad(lines, '38').variables)

def test_part():
    input = [
        'inp w',
        'mul x 0', #x = 0
        'add x z', # x = z
        'mod x 26',
        'div z 1', #1 26
        'add x 10', #10, 12, 11, 13 pour #26 : -16, -11, -13, -8, -1, -4, -14
        'eql x w',
        'eql x 0',
        'mul y 0',
        'add y 25',
        'mul y x',
        'add y 1',
        'mul z y',
        'mul y 0',
        'add y w',
        'add y 12', #12, 7, 8, 15, 13, 3, 9, 4
        'mul y x',
        'add z y',
        'inp w',
        'mul x 0',
        'add x z',
        'mod x 26',
        'div z 1',
        'add x 12',
        'eql x w',
        'eql x 0',
        'mul y 0',
        'add y 25',
        'mul y x',
        'add y 1',
        'mul z y',
        'mul y 0',
        'add y w',
        'add y 7',
        'mul y x',
        'add z y',
        'inp w',
        'mul x 0',
        'add x z',
        'mod x 26',
        'div z 1',
        'add x 10',
        'eql x w',
        'eql x 0',
        'mul y 0',
        'add y 25',
        'mul y x',
        'add y 1',
        'mul z y',
        'mul y 0',
        'add y w',
        'add y 8',
        'mul y x',
        'add z y',
    ]
    input = [l.split(' ') for l in input]
    # x = 1, y = 12+w1, z=12+w1, w1
    # x = 1, y = 5+w2, z=(320+26*w1)+w2-1, w2
    # x = 1, y = 8+w3, z=(8329+w1*676+26*w2)+w3-1, w2
    alu = Alu('333')
    try:
        for line in input:
            alu.parse_line(line)
    except Exception:
        pass
    print(alu.variables)
