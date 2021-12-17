def test_computes_y():
    ship = Spaceship((6, 3), [])
    assert ship.compute_n_for_y(1) == 3
    assert ship.compute_n_for_y(2) == 5
    assert ship.compute_n_for_y(3) == 6
    assert ship.compute_n_for_y(4) == 6
    assert ship.compute_n_for_y(5) == 5
    assert ship.compute_n_for_y(6) == 3
    assert ship.compute_n_for_y(7) == 0
    assert ship.compute_n_for_y(8) == -4


def test_computes_x():
    ship = Spaceship((6, 3), [])
    assert ship.compute_n_for_x(1) == 6
    assert ship.compute_n_for_x(2) == 11
    assert ship.compute_n_for_x(3) == 15
    assert ship.compute_n_for_x(4) == 18
    assert ship.compute_n_for_x(5) == 20
    assert ship.compute_n_for_x(6) == 21
    assert ship.compute_n_for_x(7) == 21
    assert ship.compute_n_for_x(8) == 21


def test_min_x():
    assert find_min_x(20) == 6
    assert find_min_x(138) == 17


def launch_ship(target, velocity):
    ship = Spaceship(velocity, target)
    while (ship.in_bound() and not ship.in_target()):
        ship.step()
    return ship


def find_min_x(target_min_x):
    result = 0
    n = 0
    while result < target_min_x:
        n += 1
        result = compute_step(n, n)
    return n


def test_find_max_height_real_input():
    target = Target([138, 184, -71, -125])
    in_target = find_ships_in_target(target)
    assert max([ship.max_y() for ship in in_target]) == 7750
    assert len(in_target) == 4120


def test_find_max_height():
    target = Target([20, 30, -5, -10])
    in_target = find_ships_in_target(target)
    assert max([ship.max_y() for ship in in_target]) == 45
    assert len(in_target) == 112


def find_ships_in_target(target):
    ships = set()
    min_x = find_min_x(target.min_x)
    max_x = target.max_x
    for vel_x in range(min_x, max_x + 1):
        for vel_y in range(target.max_y - 1, abs(target.max_y) + 1):
            ship = launch_ship(target, (vel_x, vel_y))
            if ship.in_target():
                ships.add(ship)
    return ships


def test_launch_ship():
    target = Target([20, 30, -5, -10])
    assert launch_ship(target, (7, 2)).max_y() == 3
    assert launch_ship(target, (6, 3)).max_y() == 6
    assert launch_ship(target, (9, 0)).max_y() == 0
    assert launch_ship(target, (17, -4)).max_y() == -4


def test_reach_target():
    target = Target([20, 30, -5, -10])
    assert launch_ship(target, (7, 2)).in_target() is True
    assert launch_ship(target, (6, 3)).in_target() is True
    assert launch_ship(target, (9, 0)).in_target() is True
    assert launch_ship(target, (17, -4)).in_target() is False


class Spaceship:

    def __init__(self, velocity, target) -> None:
        self.position = (0, 0)
        self.velocity = velocity
        self.y_pos = set()
        self.n = 0
        self.target = target

    def step(self):
        self.n += 1
        self.position = (self.compute_n_for_x(self.n), self.compute_n_for_y(self.n))
        self.y_pos.add(self.position[1])

    def in_bound(self):
        return self.position[0] <= self.target.max_x \
               and self.position[1] >= self.target.max_y

    def in_target(self):
        return self.in_bound() and self.position[0] >= self.target.min_x \
               and self.position[1] <= self.target.min_y

    def compute_n_for_y(self, n):
        return compute_step(self.velocity[1], n)

    def compute_n_for_x(self, n):
        velocity_x = self.velocity[0]
        if n > velocity_x:
            return compute_step(velocity_x, velocity_x)
        else:
            return compute_step(velocity_x, n)

    def max_y(self):
        return max(self.y_pos)


def compute_step(velocity, n):
    return int(n * velocity - (n * (n - 1)) / 2)


class Target:
    def __init__(self, target) -> None:
        self.min_x = target[0]
        self.max_x = target[1]
        self.min_y = target[2]
        self.max_y = target[3]
