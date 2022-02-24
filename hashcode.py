import numpy as np

from utils.file_utils import get_lines



def test_read_input():
    hash_code("b_better_start_small.in.txt")
    #hash_code("a_an_example.in.txt")


def hash_code(input_file):
    input = get_lines(input_file)
    line1 = input[0].split(' ')
    nb_gens = int(line1[0])
    nb_projets = int(line1[1])
    persons = list()
    projects = list()
    line = 1
    for _ in range(nb_gens):
        gen = input[line].split(' ')
        name = gen[0]
        nb_technos = int(gen[1])
        line += 1
        person = Person(name, nb_technos)
        persons.append(person)
        for _ in range(nb_technos):
            tech = input[line].split(' ')
            techno = tech[0]
            niveau = int(tech[1])
            person.add_techno(techno, niveau)
            line += 1
    for _ in range(nb_projets):
        proj = input[line].split(' ')
        project = Project(proj[0], int(proj[1]), int(proj[2]), int(proj[3]), int(proj[4]))
        projects.append(project)
        line += 1
        for _ in range(int(proj[4])):
            tech = input[line].split(' ')
            techno = tech[0]
            niveau = int(tech[1])
            project.add_techno(techno, niveau)
            line += 1
    print()

    outputs = list()
    for project in projects:
        output = Output(project.name)
        for techno in project.technos.keys():
            for person in persons:
                if techno in person.technos.keys() and person.technos[techno] >= project.technos[techno]:
                    output.add_person(person.name)
        if len(output.persons) > 0:
            outputs.append(output)

    print(len(outputs))
    for output in outputs:
        output.print()

class Output:

    def __init__(self, project_name) -> None:
        super().__init__()
        self.project_name = project_name
        self.persons = list()

    def add_person(self, name):
        self.persons.append(name)

    def print(self):
        print(self.project_name)
        print(' '.join(self.persons))



class Person:
    def __init__(self, name, nb_technos) -> None:
        self.name = name
        self.nb_technos = nb_technos
        self.technos = dict()

    def add_techno(self, techno, level):
        self.technos[techno] = level


class Project:
    def __init__(self, name, length, score, best_before, nb_technos) -> None:
        super().__init__()
        self.name = name
        self.technos = dict()
        self.length = length
        self.score = score
        self.best_before = best_before
        self.nb_technos = nb_technos

    def add_techno(self, techno, level):
        self.technos[techno] = level
