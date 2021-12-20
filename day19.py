from collections import namedtuple

from utils.file_utils import get_lines


class Scanner:

    def __init__(self, counter) -> None:
        self.number = counter
        self.beacons = list()
        self.arrangements = list()

    def add_beacon(self, line):
        self.beacons.append(tuple([int(coord) for coord in line.split(',')]))

    def compute_rotations(self):
        for beacon in self.beacons:
            self.arrangements.append(permutations(beacon))

    def get_arrangement(self, index):
        return [arrangement[index] for arrangement in self.arrangements]

    def find_common_beacons(self, other_scanner):
        for beacon in self.beacons:
            for j in range(len(other_scanner.arrangements[0])):
                other_arrangement = other_scanner.get_arrangement(j)
                for other_beacon in other_arrangement:
                    translation_point = compute_translation_point(beacon, other_beacon)
                    translation = translate(other_arrangement, translation_point)
                    if len(translation.intersection(self.beacons)) >= 12:
                        return translation_point, translation
        return None, None


def compute_translation_point(beacon, other_beacon):
    translation_point = (beacon[0] - other_beacon[0],
                         beacon[1] - other_beacon[1],
                         beacon[2] - other_beacon[2])
    return translation_point


def translate(other_beacons, translation_point):
    translation = set()
    for beacon in other_beacons:
        translation.add(
            (beacon[0] + translation_point[0], beacon[1] + translation_point[1], beacon[2] + translation_point[2]))
    return translation


def test_rotations():
    assert len(permutations(tuple([1, 2, 3]))) == 24


def permutations(coords):
    result = list()
    Coords = namedtuple('Coords', 'x y z')
    named = Coords(coords[0], coords[1], coords[2])
    result.append((named.z, named.x, named.y))
    result.append((named.y, named.x, -named.z))
    result.append((-named.z, named.x, -named.y))
    result.append((-named.y, named.x, named.z))
    result.append((named.y, -named.x, named.z))
    result.append((named.z, -named.x, -named.y))
    result.append((-named.y, -named.x, -named.z))
    result.append((-named.z, -named.x, named.y))
    result.append((named.x, named.y, named.z))
    result.append((named.x, -named.z, named.y))
    result.append((named.x, -named.y, -named.z))
    result.append((named.x, named.z, -named.y))
    result.append((-named.x, named.y, -named.z))
    result.append((-named.x, named.z, named.y))
    result.append((-named.x, -named.y, named.z))
    result.append((-named.x, -named.z, -named.y))
    result.append((-named.z, named.y, named.x))
    result.append((named.y, named.z, named.x))
    result.append((named.z, -named.y, named.x))
    result.append((-named.y, -named.z, named.x))
    result.append((named.z, named.y, -named.x))
    result.append((-named.y, named.z, -named.x))
    result.append((-named.z, -named.y, -named.x))
    result.append((named.y, -named.z, -named.x))
    return list(dict.fromkeys(result))


def test_parse_input():
    input = get_lines('day19.txt')
    scanners = parse_input(input)
    assert len(scanners) == 26
    scanners[0].compute_rotations()
    print(scanners[0].get_arrangement(0))


def test_find_common_beacons():
    input = get_lines('day19_sample.txt')
    distances_to_ref, known_beacons = find_mutual_references(input)
    assert len(known_beacons) == 79
    assert compute_manhattan_distances(distances_to_ref) == 3621


def test_find_common_beacons_real():
    input = get_lines('day19.txt')
    distances_to_ref, known_beacons = find_mutual_references(input)
    assert len(known_beacons) == 320
    assert compute_manhattan_distances(distances_to_ref) == 9655


def find_mutual_references(input):
    scanners = parse_input(input)
    scanners_to_find = list()
    scanners_to_find.extend(scanners[1:])
    found_scanners = list()
    found_scanners.append(scanners[0])
    known_beacons = set(scanners[0].beacons)
    distances_to_ref = list()
    while len(scanners_to_find) > 0:
        for reference_scanner in found_scanners:
            for other_scanner in scanners_to_find:
                translation_point, translated_beacons = reference_scanner.find_common_beacons(other_scanner)
                if translation_point:
                    known_beacons.update(translated_beacons)
                    other_scanner.beacons = translated_beacons
                    scanners_to_find.remove(other_scanner)
                    found_scanners.append(other_scanner)
                    distances_to_ref.append(translation_point)
    return distances_to_ref, known_beacons


def test_manhattan():
    tuples = list()
    tuples.append((68, -1246, -43))
    tuples.append((-92, -2380, -20))
    tuples.append((-20, -1133, 1061))
    tuples.append((1105, -1205, 1229))
    assert compute_manhattan_distances(tuples) == 3621


def compute_manhattan_distances(tuples):
    distances = set()
    for index, tuple in enumerate(tuples):
        for other_tuple in tuples[index + 1:]:
            distances.add(
                abs(tuple[0] - other_tuple[0]) + abs(tuple[1] - other_tuple[1]) + abs(tuple[2] - other_tuple[2]))
    return max(distances)


def parse_input(input):
    scanners = list()
    scanners_count = 0

    for line in input:
        if line.find('---') >= 0:
            current_scanner = Scanner(scanners_count)
            scanners.append(current_scanner)
            scanners_count += 1
        elif len(line) != 0:
            current_scanner.add_beacon(line)
        else:
            current_scanner.compute_rotations()
    current_scanner.compute_rotations()
    return scanners
