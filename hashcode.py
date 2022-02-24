import numpy as np

from utils.file_utils import get_lines


def main():
    hash_code("b_better_start_small.in.txt")

if __name__ == "__main__":
    main()


def test_read_input():
    hash_code("c_collaboration.in.txt")
    hash_code("d_dense_schedule.in.txt")
    hash_code("e_exceptional_skills.in.txt")
    hash_code("f_find_great_mentors.in.txt")
    hash_code("a_an_example.in.txt")
    hash_code("b_better_start_small.in.txt")


def hash_code(input_file):
    f = open(input_file+"output.txt", "w")

    input = get_lines(input_file)
    line1 = input[0].split(' ')
    nb_gens = int(line1[0])
    nb_projets = int(line1[1])
    persons = set()
    persone_by_name = dict()
    projects = set()
    line = 1
    for _ in range(nb_gens):
        gen = input[line].split(' ')
        name = gen[0]
        nb_technos = int(gen[1])
        line += 1
        person = Person(name, nb_technos)
        persons.add(person)
        persone_by_name[name] = person
        for _ in range(nb_technos):
            tech = input[line].split(' ')
            techno = tech[0]
            niveau = int(tech[1])
            person.add_techno(techno, niveau)
            line += 1
    for _ in range(nb_projets):
        proj = input[line].split(' ')
        project = Project(proj[0], int(proj[1]), int(proj[2]), int(proj[3]), int(proj[4]))
        projects.add(project)
        line += 1
        for _ in range(int(proj[4])):
            tech = input[line].split(' ')
            techno = tech[0]
            niveau = int(tech[1])
            project.add_techno(techno, niveau)
            line += 1

    outputs = list()
    for project in sorted(projects):
        project_to_count = True
        output = Output(project.name)
        for skill in project.techno_skills:
            find = False
            filtered_persons = (person for person in persons if skill.techno in person.technos and skill.level <= person.technos[skill.techno])
            for person in sorted(filtered_persons):
                if person.name not in output.persons and skill.techno in person.technos.keys() and person.technos[skill.techno] >= skill.level:
                    output.add_person(skill.techno, person.name)
                    find = True
                    break
            if find is False:
                project_to_count = False
                break

        if len(output.persons) > 0 and project_to_count:
            outputs.append(output)
            for techno in output.techno_person.keys():
                person = persone_by_name[output.techno_person[techno]]
                if project.technos[techno] == person.technos[techno]:
                    person.technos[techno] += 1
                    person.nb_projects += 1

    f.write(str(len(outputs))+"\n")
    for output in outputs:
        output.print(f)

    f.close()

class Output:

    def __init__(self, project_name) -> None:
        super().__init__()
        self.project_name = project_name
        self.persons = set()
        self.techno_person = dict()
        self.ordered_persons = list()

    def add_person(self, techno, name):
        if name not in self.persons:
            self.persons.add(name)
            self.techno_person[techno] = name
            self.ordered_persons.append(name)

    def print(self, file):
           file.write(self.project_name+"\n")
           file.write(' '.join(self.ordered_persons)+"\n")



class Person:
    def __init__(self, name, nb_technos) -> None:
        self.name = name
        self.nb_technos = nb_technos
        self.technos = dict()
        self.nb_projects = 1

    def add_techno(self, techno, level):
        self.technos[techno] = level

    def __gt__(self, other):
        return sum(self.technos.values())*self.nb_projects > sum(other.technos.values())*other.nb_projects


class Project:
    def __init__(self, name, length, score, best_before, nb_technos) -> None:
        super().__init__()
        self.name = name
        self.technos = dict()
        self.length = length
        self.score = score
        self.best_before = best_before
        self.nb_technos = nb_technos
        self.techno_skills = list()

    def add_techno(self, techno, level):
        self.techno_skills.append(ProjectSkill(techno, level))
        if techno in self.technos:
            self.technos[techno].append(level)
        else:
            levels = list()
            levels.append(level)
            self.technos[techno] = levels

    def __gt__(self, other):
        return self.score * self.score / self.length / self.best_before < other.score * other.score / other.length / other.best_before

class ProjectSkill:
    def __init__(self, techno, level) -> None:
        super().__init__()
        self.techno = techno
        self.level = level


