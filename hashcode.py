import numpy as np

from utils.file_utils import get_lines


def test_read_input():
    input = get_lines("a_an_example.in.txt")

    line1 = input[0].split(' ')
    nb_gens = int(line1[0])
    nb_projets = int(line1[1])


    line = 1
    for i in range(nb_gens):
        gen = input[line].split(' ')
        name = gen[0]
        nb_technos = int(gen[1])
        line += 1
        for j in range(nb_technos):
            tech = input[line].split(' ')
            techno = tech[0]
            niveau = tech[1]
            line +=1

    for i in range(nb_projets):
        pass