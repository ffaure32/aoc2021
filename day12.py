import collections
import copy

from utils.file_utils import get_lines


def test_parse_input_first_sample():
    lines = [
        'start - A',
        'start - b',
        'A - c',
        'A - b',
        'b - d',
        'A - end',
        'b - end']

    all_pathes = compute_all_pathes(lines)

    #assert all_pathes.count_valid() == 10
    assert all_pathes.count_valid() == 36


def test_parse_input_second_sample():
    lines = [
        'dc - end',
        'HN - start',
        'start - kj',
        'dc - start',
        'dc - HN',
        'LN - dc',
        'HN - end',
        'kj - sa',
        'kj - HN',
        'kj - dc',
    ]
    all_pathes = compute_all_pathes(lines)
    #assert all_pathes.count_valid() == 19
    assert all_pathes.count_valid() == 103


def test_parse_input_third_sample():
    lines = [
        'fs - end',
        'he - DX',
        'fs - he',
        'start - DX',
        'pj - DX',
        'end - zg',
        'zg - sl',
        'zg - pj',
        'pj - he',
        'RW - he',
        'fs - DX',
        'pj - RW',
        'zg - RW',
        'start - pj',
        'he - WI',
        'zg - he',
        'pj - fs',
        'start - RW',
    ]

    all_pathes = compute_all_pathes(lines)

    #assert all_pathes.count_valid() == 226
    assert all_pathes.count_valid() == 3509


def test_parse_input():
    lines = get_lines('day12.txt')
    all_pathes = compute_all_pathes(lines)

    #assert all_pathes.count_valid() == 4411
    assert all_pathes.count_valid() == 136767


def compute_all_pathes(lines):
    segments = set()
    for line in lines:
        split = line.split('-')
        split = [x.strip(' ') for x in split]
        elements = frozenset(split)
        segments.add(elements)
    start_points = {seg for seg in segments if 'start' in seg}
    all_pathes = AllPathes()
    for start_point in start_points:
        new_path = Path(start_point, segments)
        all_pathes.add(new_path)
    finished = False
    while not finished:
        all_pathes.next_segment()
        finished = all_pathes.is_finished()
    return all_pathes


def get_other_point_for_segment(segment, point):
    list_of_points = list(segment)
    if list_of_points[0] == point:
        return list_of_points[1]
    else:
        return list_of_points[0]


class AllPathes():
    def __init__(self) -> None:
        self.pathes = set()
        self.already_managed = set()

    def add(self, path):
        self.pathes.add(path)

    def next_segment(self):
        ongoing_pathes = {path for path in self.pathes if path.is_not_finished()}
        for path in ongoing_pathes:
            self.pathes.remove(path)
            if path not in self.already_managed:
                new_pathes = path.new_pathes()
                for new_path in new_pathes:
                    if new_path not in self.already_managed and new_path.is_valid():
                        self.pathes.add(new_path)
                self.already_managed.add(path)

    def is_finished(self):
        return len({path for path in self.pathes if path.is_not_finished()}) == 0

    def count_valid(self):
        return len({path for path in self.pathes if path.is_valid()})


class Path:
    def __eq__(self, other: object) -> bool:
        return (self.__class__ == other.__class__ and
                self.path == other.path
                )

    def __hash__(self) -> int:
        return str(self.path).__hash__()

    def __str__(self) -> str:
        return str(self.path)

    def __init__(self, first_segment, all_segments) -> None:
        super().__init__()
        self.all_segments = all_segments
        self.oriented_segments = list()
        self.path = list()
        next_point = get_other_point_for_segment(first_segment, 'start')
        self.path.append('start')
        self.path.append(next_point)
        self.oriented_segments.append(['start', next_point])

    def is_not_finished(self):
        return self.path[-1] != 'end'

    def new_pathes(self):
        new_pathes = set()
        last_point = self.path[-1]
        new_ways = {seg for seg in self.all_segments if last_point in seg}
        for new_way in new_ways:
            oriented_segment = [last_point, get_other_point_for_segment(new_way, last_point)]
            if oriented_segment[1] != 'start':
                new_path = copy.deepcopy(self)
                new_path.path.append(oriented_segment[1])
                new_path.oriented_segments.append(oriented_segment)
                new_pathes.add(new_path)
        return new_pathes

    def is_valid(self):
        point_count = collections.Counter(self.path)
        lower_point_count = {key:value for (key, value) in point_count.items() if key.lower() == key}
        values_count = collections.Counter(lower_point_count.values())
        if len([key for key in values_count.keys() if key >2]) > 0:
            return False
        if values_count[2] > 1:
            return False
        return True

    def old_valid(self):
        point_count = collections.Counter(self.path)
        for key in point_count.keys():
            if key.lower() == key and point_count[key] > 1:
                return False
        return True
