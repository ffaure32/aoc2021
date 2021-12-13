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

    # assert all_pathes.count_valid() == 10
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
    # assert all_pathes.count_valid() == 19
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

    # assert all_pathes.count_valid() == 226
    assert all_pathes.count_valid() == 3509


def test_parse_input():
    lines = get_lines('day12.txt')
    all_pathes = compute_all_pathes(lines)

    # assert all_pathes.count_valid() == 4411
    assert all_pathes.count_valid() == 136767


def compute_all_pathes(lines):
    segments = set()
    for line in lines:
        split = line.split('-')
        split = [x.strip(' ') for x in split]
        elements = frozenset(split)
        segments.add(elements)
    start_points = {seg for seg in segments if 'start' in seg}
    all_pathes = AllPathes(segments)
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
    def __init__(self, segments) -> None:
        self.pathes = set()
        self.segments = segments

    def add(self, path):
        self.pathes.add(path)

    def next_segment(self):
        ongoing_pathes = {path for path in self.pathes if path.is_not_finished()}
        for path in ongoing_pathes:
            self.pathes.remove(path)
            new_pathes = path.new_pathes(self.segments)
            for new_path in new_pathes:
                if new_path.is_valid():
                    self.pathes.add(new_path)

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
        self.lower_pass = set()
        self.lower_double = False
        self.valid = True
        self.path = list()
        next_point = get_other_point_for_segment(first_segment, 'start')
        self.add_path('start')
        self.add_path(next_point)

    def is_not_finished(self):
        return self.path[-1] != 'end'

    def new_pathes(self, all_segments):
        new_pathes = set()
        last_point = self.path[-1]
        new_ways = {seg for seg in all_segments if last_point in seg}
        for new_way in new_ways:
            oriented_segment = [last_point, get_other_point_for_segment(new_way, last_point)]
            if oriented_segment[1] != 'start':
                new_path = copy.deepcopy(self)
                new_path.add_path(oriented_segment[1])
                if new_path.is_valid():
                    new_pathes.add(new_path)
        return new_pathes

    def add_path(self, point):
        if point == point.lower():
            if point in self.lower_pass:
                if self.lower_double:
                    self.valid = False
                else:
                    self.lower_double = True
            self.lower_pass.add(point)
        self.path.append(point)

    def is_valid(self):
        return self.valid

    def old_valid(self):
        point_count = collections.Counter(self.path)
        for key in point_count.keys():
            if key.lower() == key and point_count[key] > 1:
                return False
        return True
