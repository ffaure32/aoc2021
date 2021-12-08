from utils.file_utils import get_lines


def test_input():
    lines = get_lines('day7.txt')
    crabs = [int(dist) for dist in lines[0].split(',')]
    distances = dict()
    for i in range(min(crabs), max(crabs)):
        distances[i] = 0
        for crab in crabs:
            distances[i] += compute_dist(abs(crab - i))
    assert min(distances.values()) == 92676646


def test_comput_dist():
    assert 6 == compute_dist(3)

computed_dists = dict()
def compute_dist(steps):
    if steps in computed_dists:
        return computed_dists[steps]
    result = 0
    for i in range(steps+1):
        result += i
    computed_dists[steps] = result
    return result