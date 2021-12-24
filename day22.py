from utils.file_utils import get_lines


def test_basic_sample():
    input = [
        'on x=10..12,y=10..12,z=10..12',
        'on x=11..13,y=11..13,z=11..13',
        'off x=9..11,y=9..11,z=9..11',
        'on x=10..10,y=10..10,z=10..10'
    ]
    assert parse_input(input) == 39


def test_parse_input():
    pass
    #input = get_lines('day22_sample.txt')
    #assert parse_input(input) == 590784


def test_parse_input_real():
    pass
    #input = get_lines('day22.txt')
    #assert parse_input(input) == 580098


def parse_input(input):
    cuboids = [Cuboid(line) for line in input]
    region = Region(50, cuboids)
    region.initialization()
    return region.count_on_cubes()


def parse_line(line):
    Cuboid(line)


class Cuboid:
    def __init__(self, line=None, x_tuple=None, y_tuple=None, z_tuple=None, turn_on = 0) -> None:
        if line:
            split = line.split(' ')
            if split[0] == 'on':
                self.turn_on = 1
            else:
                self.turn_on = 0
            coords = split[1].split(',')
            self.min_x, self.max_x = [int(c) for c in coords[0].split('=')[1].split('..')]
            self.min_y, self.max_y = [int(c) for c in coords[1].split('=')[1].split('..')]
            self.min_z, self.max_z = [int(c) for c in coords[2].split('=')[1].split('..')]
        else:
            self.min_x, self.max_x = x_tuple
            self.min_y, self.max_y = y_tuple
            self.min_z, self.max_z = z_tuple
            self.turn_on = turn_on

    def x_tuple(self):
        return self.min_x, self.max_x

    def y_tuple(self):
        return self.min_y, self.max_y

    def z_tuple(self):
        return self.min_z, self.max_z

    def __eq__(self, o: object) -> bool:
        return type(o) is Cuboid and self.x_tuple() == o.x_tuple() and self.y_tuple() == o.y_tuple() and self.z_tuple() == o.z_tuple()

    def __hash__(self) -> int:
        return hash((self.x_tuple(), self.y_tuple(), self.z_tuple()))

    def volume(self):
        return (abs(self.max_x-self.min_x)+1) * (abs(self.max_y-self.min_y)+1) * (abs(self.max_z-self.min_z)+1)

def test_eq_cub():
    cub1 = Cuboid(None, (2,3),(3,4),(4,5))
    cub2 = Cuboid(None, (2, 3), (3, 4), (4, 5))
    assert cub1 == cub2

class Region:
    def __init__(self, max_coords=None, cuboids=None) -> None:
        self.max_coords = max_coords
        self.cuboids = cuboids
        self.region = self.init_region()

    def init_region(self):
        dict_z = dict()
        range_coords = range(-self.max_coords, self.max_coords + 1)
        for z in range_coords:
            dict_y = dict()
            dict_z[z] = dict_y
            for y in range_coords:
                dict_x = dict()
                dict_y[y] = dict_x
                for x in range_coords:
                    dict_x[x] = 0
        return dict_z

    def initialization(self):
        for cuboid in self.cuboids:
            for z in self.init_range(cuboid.min_z, cuboid.max_z):
                for y in self.init_range(cuboid.min_y, cuboid.max_y):
                    for x in self.init_range(cuboid.min_x, cuboid.max_x):
                        self.region[x][y][z] = cuboid.turn_on

    def count_on_cubes(self):
        range_coords = range(-self.max_coords, self.max_coords + 1)
        total = 0
        for z in range_coords:
            for y in range_coords:
                total += sum(self.region[z][y].values())
        return total

    def init_range(self, min_c, max_c):
        if min_c > self.max_coords and max_c > self.max_coords or min_c < -self.max_coords and max_c < - self.max_coords:
            return range(0, 0)
        return range(self.abs_coord(min_c), self.abs_coord(max_c) + 1)

    def abs_coord(self, min_c):
        if min_c >= self.max_coords:
            min_r = self.max_coords
        elif min_c <= -self.max_coords:
            min_r = -self.max_coords
        else:
            min_r = min_c
        return min_r


def test_segments_intersect_left():
    seg_1 = (3, 7)
    seg_2 = (4, 10)
    result = segments_intersect_and_diff(seg_1, seg_2)
    assert result.inters == (4, 7)
    assert (3, 3) in result.diffs
    assert (8, 10) not in result.diffs


def test_segments_intersect_right():
    seg_1 = (7, 15)
    seg_2 = (4, 10)
    result = segments_intersect_and_diff(seg_1, seg_2)
    assert result.inters == (7, 10)
    assert (4, 6) not in result.diffs
    assert (11, 15) in result.diffs


def test_first_left():
    seg_1 = (7, 15)
    seg_2 = (18, 20)
    result = segments_intersect_and_diff(seg_1, seg_2)
    assert result.inters is None
    assert (7, 15) in result.diffs


def test_first_right():
    seg_1 = (18, 20)
    seg_2 = (7, 15)
    result = segments_intersect_and_diff(seg_1, seg_2)
    assert result.inters is None
    assert (18, 20) in result.diffs


def test_segments_intersect_included():
    seg_1 = (5, 7)
    seg_2 = (4, 10)
    result = segments_intersect_and_diff(seg_1, seg_2)
    assert result.inters == (5, 7)
    assert len(result.diffs) == 0


def test_bigger():
    seg_1 = (4, 20)
    seg_2 = (7, 15)
    result = segments_intersect_and_diff(seg_1, seg_2)
    assert result.inters == (7, 15)
    assert (4, 6) in result.diffs
    assert (16, 20) in result.diffs


def test_same():
    seg_1 = (7, 15)
    seg_2 = (7, 15)
    result = segments_intersect_and_diff(seg_1, seg_2)
    assert result.inters == (7, 15)
    assert len(result.diffs) == 0


def turn_off_inside():
    left = Cuboid('on x=11..13,y=11..13,z=11..13')
    right = Cuboid('on x=10..15,y=10..15,z=10..15')
    result = explode_rectange(left, right)
    assert len(result) == 0


def test_explode_coin():
    left = Cuboid('on x=8..13,y=8..13,z=8..13')
    right = Cuboid('on x=10..15,y=10..15,z=10..15')
    result = explode_rectange(left, right)
    assert len(result) == 7


def test_explode_coin_outside():
    left = Cuboid('on x=10..15,y=10..15,z=10..15')
    right = Cuboid('on x=11..13,y=8..13,z=11..13')
    result = explode_rectange(left, right)
    assert len(result) == 17


def test_explode_outside():
    left = Cuboid('on x=10..15,y=10..15,z=10..15')
    right = Cuboid('on x=11..13,y=11..13,z=11..13')
    result = explode_rectange(left, right)
    assert len(result) == 26


def explode_rectange(rectangle_to_keep: Cuboid, rectangle_to_remove: Cuboid):
    x_diff = segments_intersect_and_diff(rectangle_to_keep.x_tuple(), rectangle_to_remove.x_tuple())
    y_diff = segments_intersect_and_diff(rectangle_to_keep.y_tuple(), rectangle_to_remove.y_tuple())
    z_diff = segments_intersect_and_diff(rectangle_to_keep.z_tuple(), rectangle_to_remove.z_tuple())
    result = set()
    for x_seg in x_diff.all_segs():
        for y_seg in y_diff.all_segs():
            for z_seg in z_diff.all_segs():
                if x_seg != x_diff.inters or y_seg != y_diff.inters or z_seg != z_diff.inters:
                    result.add(Cuboid(None, x_seg, y_seg, z_seg))
    if len(result) == 0 and (x_diff.inters == None or y_diff.inters == None or z_diff.inters == None) :
        result.add(Cuboid(None, rectangle_to_keep.x_tuple(), rectangle_to_keep.y_tuple(), rectangle_to_keep.z_tuple()))

    return result


def segments_intersect_and_diff(to_keep, to_remove):
    result = SegmentDiff()

    if to_keep[1] < to_remove[0]:
        result.add_diff(to_keep)
    elif to_keep[0] > to_remove[1]:
        result.add_diff(to_keep)
    elif to_keep[1] < to_remove[1]:
        if to_keep[0] < to_remove[0]:
            result.add_diff((to_keep[0], to_remove[0] - 1))
            result.inters = (to_remove[0], to_keep[1])
        else:
            result.inters = to_keep
    elif to_keep[0] > to_remove[0]:
        if to_keep[1] != to_remove[1]:
            result.add_diff((to_remove[1] + 1, to_keep[1]))
        result.inters = (to_keep[0], to_remove[1])
    else:
        if to_keep[0] != to_remove[0]:
            result.add_diff((to_keep[0], to_remove[0] - 1))
        if to_keep[1] != to_remove[1]:
            result.add_diff((to_remove[1] + 1, to_keep[1]))
        result.inters = to_remove
    return result


class SegmentDiff:
    def __init__(self) -> None:
        self.diffs = set()
        self.inters = None

    def add_diff(self, segment):
        self.diffs.add(segment)

    def all_segs(self):
        all_segs = set()
        if self.inters:
            all_segs.add(self.inters)
            all_segs.update(self.diffs)
        return all_segs


def turn_off(on_cuboids, cuboid):
    new_on_cuboids = set()
    for on_cuboid in on_cuboids:
        new_on_cuboids.update(explode_rectange(on_cuboid, cuboid))
    return new_on_cuboids


def merge_on_cuboids(merged_cuboids, on_cuboid):
    to_merge_set = set()
    to_merge_set.add(on_cuboid)
    for merged_cuboid in merged_cuboids:
        to_merge_set.update(explode_rectange(merged_cuboid, on_cuboid))
    return to_merge_set


def merge_two_by_two(cuboid1, cuboid2):
    merged = set()
    merged.update(merge(cuboid1, cuboid2))
    merged.update(merge(cuboid2, cuboid1))
    return merged


def parse_input_part2(input):
    cuboids = [Cuboid(line) for line in input]
    on_cuboids = set()
    for cuboid in cuboids:
        if cuboid.turn_on:
            on_cuboids = merge_on_cuboids(on_cuboids, cuboid)
        else:
            on_cuboids = turn_off(on_cuboids, cuboid)
    return on_cuboids

def test_parse_input_part2():
     input = get_lines('day22_part2.txt')
     final_on_cuboids = parse_input_part2(input)
     assert sum(cub.volume() for cub in final_on_cuboids) == 2758514936282235



def test_parse_input_part2_real():
     input = get_lines('day22.txt')
     final_on_cuboids = parse_input_part2(input)
     assert sum(cub.volume() for cub in final_on_cuboids) == 1134725012490723


def test_parse_input_simple_include():
    input = list()
    input.append('on x=0..2,y=0..2,z=0..2')
    input.append('off x=1..1,y=1..1,z=1..1')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 26


def test_parse_input_simple_off_distant():
    input = list()
    input.append('on x=0..1,y=0..1,z=0..1')
    input.append('off x=3..4,y=3..4,z=3..4')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 8


def test_parse_input_simple_on_distant():
    input = list()
    input.append('on x=0..1,y=0..1,z=0..1')
    input.append('on x=3..4,y=3..4,z=3..4')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 16


def test_parse_input_simple_off_side_by_side():
    input = list()
    input.append('on x=0..1,y=0..1,z=0..1')
    input.append('off x=1..2,y=0..1,z=0..1')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 4

def test_parse_input_simple_off_everythong():
    input = list()
    input.append('on x=0..1,y=0..1,z=0..1')
    input.append('off x=1..2,y=0..1,z=0..1')
    input.append('off x=0..0,y=0..1,z=0..1')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 0


def test_parse_input_simple_side_by_side():
    input = list()
    input.append('on x=0..3,y=0..3,z=0..3')
    input.append('on x=3..6,y=0..3,z=0..3')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 112


def test_parse_input_simple_side_by_side_off():
    input = list()
    input.append('on x=4..4,y=0..1,z=0..1')
    input.append('on x=2..2,y=0..1,z=0..1')
    input.append('on x=0..1,y=0..1,z=0..1')
    input.append('off x=-1..1,y=-1..1,z=-1..1')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 8

def test_parse_input_simple_side_by_side_without_off():
    input = list()
    input.append('on x=0..1,y=0..1,z=0..1')
    input.append('on x=1..2,y=0..1,z=0..1')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 12

def test_merge_inside_cube():
    input = list()
    input.append('on x=1..2,y=1..2,z=1..2')
    input.append('on x=0..3,y=0..3,z=0..3')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 64

def test_merge_exclude_inside_cube():
    input = list()
    input.append('on x=0..3,y=0..3,z=0..3')
    input.append('off x=1..2,y=1..2,z=1..2')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 56


def test_merge_exclude_inside_cube_corner():
    input = list()
    input.append('on x=0..3,y=0..3,z=0..3')
    input.append('off x=-1..1,y=-1..1,z=-1..1')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 56


def test_merge_equal():
    input = list()
    input.append('on x=0..1,y=0..1,z=0..1')
    input.append('on x=0..1,y=0..1,z=0..1')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 8

def test_merge_equal_2():
    input = list()
    input.append('on x=0..0,y=0..0,z=0..0')
    input.append('on x=0..1,y=0..1,z=0..1')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 8


def test_merge_equal_2_1():
    input = list()
    input.append('on x=0..0,y=0..0,z=0..0')
    input.append('on x=0..2,y=0..1,z=0..1')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 12


def test_merge_equal_3():
    input = list()
    input.append('on x=0..2,y=0..1,z=0..1')
    input.append('on x=0..1,y=0..1,z=0..1')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 12


def test_merge_equal_4():
    input = list()
    input.append('on x=0..2,y=0..2,z=0..2')
    input.append('on x=1..1,y=1..1,z=1..1')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 27


def test_merge_equal_5():
    input = list()
    input.append('on x=3..4,y=3..4,z=3..4')
    input.append('on x=0..1,y=0..1,z=0..1')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 16


def test_parse_input_simple_side_by_side_off_negative():
    input = list()
    input.append('on x=0..2,y=0..1,z=0..1')
    input.append('off x=-1..1,y=-1..1,z=-1..1')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 4

def test_merge_6():
    input = list()
    input.append('on x=0..1,y=0..1,z=0..1')
    input.append('on x=2..3,y=2..3,z=2..3')
    input.append('on x=4..5,y=4..5,z=4..5')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 24

def test_merge_7():
    input = list()
    input.append('on x=0..1,y=0..1,z=0..1')
    input.append('on x=1..2,y=1..2,z=1..2')
    input.append('on x=2..3,y=2..3,z=2..3')
    final_on_cuboids = parse_input_part2(input)
    assert sum(cub.volume() for cub in final_on_cuboids) == 22
