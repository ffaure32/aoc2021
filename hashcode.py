import numpy as np

from utils.file_utils import get_lines


def test_read_input():
    input = get_lines("a_an_example.in.txt")

    line1 = input[0].split(' ')
    nb_gens = int(line1[0])
    nb_projets = int(line1[1])

    persons = list()

    line = 1
    for i in range(nb_gens):
        gen = input[line].split(' ')
        name = gen[0]
        nb_technos = int(gen[1])
        line += 1
        person = Person(name)
        persons.append(person)
        for j in range(nb_technos):
            tech = input[line].split(' ')
            techno = tech[0]
            niveau = int(tech[1])
            person.add_techno(techno, niveau)
            line +=1

    for i in range(nb_projets):
        pass


class Person:
    def __init__(self, name) -> None:
        self.name = name
        self.technos = dict()

    def add_techno(self, techno, level):
        self.technos[techno] = level

class Project:
    def __init__(self, name, length, score, best_before) -> None:
        super().__init__()
        self.name = name
        self.technos = dict()
        self.length = length
        self.score = score
        self.best_before = best_before

    def add_techno(self, techno, level):
        self.technos[techno] = level
