import copy

board_size = 10


class Player:
    def __init__(self, position) -> None:
        self.position = position
        self.score = 0

    def move(self, dice):
        self.position = (self.position + dice) % board_size
        if self.position == 0:
            self.position = 10
        self.score += self.position

    def has_won(self):
        return self.score >= 1000


class Dice:
    def __init__(self) -> None:
        self.index = 0
        self.roll_count = 0

    def roll(self):
        self.increase_roll()
        roll = self.index
        self.increase_roll()
        roll += self.index
        self.increase_roll()
        roll += self.index
        self.roll_count += 3
        return roll

    def increase_roll(self):
        self.index += 1
        if self.index > 100:
            self.index = 1


def moves(pos_1, pos_2):
    player1 = Player(pos_1)
    player2 = Player(pos_2)
    dice = Dice()

    while True:
        player1.move(dice.roll())
        if player1.has_won():
            return dice.roll_count * player2.score
        player2.move(dice.roll())
        if player2.has_won():
            return dice.roll_count * player1.score


class Game:
    def __init__(self, pos_1, pos_2):
        self.players = [Player(pos_1), Player(pos_2)]
        self.dice_roll = 0

    def play_turn(self, dice_roll, player_index):
        player_turn = self.players[player_index]
        player_turn.move(dice_roll)
        if player_turn.has_won():
            return True
        self.dice_roll = 0

    def roll(self, dice_roll):
        self.dice_roll += dice_roll


def test_moves():
    result = moves(4, 8)
    assert result == 739785


def test_moves_real():
    result = moves(9, 10)
    assert result == 707784



class GameKey:
    def __init__(self, pos_1=1, pos_2=1, score_1=0, score_2=0) -> None:
        self.pos_1 = pos_1
        self.score1 = score_1
        self.pos_2 = pos_2
        self.score2 = score_2

    def move_1(self, dice_roll):
        self.pos_1 = self.compute_new_pos(self.pos_1, dice_roll)
        self.score1 += self.pos_1

    def move_2(self, dice_roll):
        self.pos_2 = self.compute_new_pos(self.pos_2, dice_roll)
        self.score2 += self.pos_2

    def compute_new_pos(self, pos, roll):
        new_pos = (pos + roll) % board_size
        if new_pos == 0:
            new_pos = board_size
        return new_pos

    def __eq__(self, o: object) -> bool:
        return type(
            o) is GameKey and self.pos_1 == o.pos_1 and self.pos_2 == o.pos_2 and self.score1 == o.score1 and self.score2 == o.score2

    def __hash__(self) -> int:
        return hash((self.pos_1, self.pos_2, self.score1, self.score2))


class NewDiracDie:

    def __init__(self, pos1, pos2) -> None:
        super().__init__()
        self.player1_wins = 0
        self.player2_wins = 0
        self.games = dict()
        self.games[GameKey(pos1, pos2)] = 1
        self.player_turn = 0

    def dirac_moves(self):
        while len(self.games) > 0:
            new_games = dict()
            for game in self.games:
                self.play_turn(game, new_games, 3, 1)
                self.play_turn(game, new_games, 4, 3)
                self.play_turn(game, new_games, 5, 6)
                self.play_turn(game, new_games, 6, 7)
                self.play_turn(game, new_games, 7, 6)
                self.play_turn(game, new_games, 8, 3)
                self.play_turn(game, new_games, 9, 1)

            if self.player_turn == 0:
                self.player_turn = 1
            else:
                self.player_turn = 0
            self.games = new_games

    def play_turn(self, game, new_games, die, occurrences):
        occ = occurrences * self.games[game]
        new_game = copy.deepcopy(game)
        if self.player_turn == 0:
            new_game.move_1(die)
            if new_game.score1 >= 21:
                self.player1_wins += occ
            else:
                self.add_game_occurences(new_game, new_games, occ)
        else:
            new_game.move_2(die)
            if new_game.score2 >= 21:
                self.player2_wins += occ
            else:
                self.add_game_occurences(new_game, new_games, occ)

    def add_game_occurences(self, new_game, new_games, occ):
        if new_game in new_games:
            new_games[new_game] += occ
        else:
            new_games[new_game] = occ


def test_dirac_moves():
    dirac = NewDiracDie(4, 8)
    dirac.dirac_moves()

    assert dirac.player2_wins == 341960390180808
    assert dirac.player1_wins == 444356092776315


def test_dirac_moves_real():
    dirac = NewDiracDie(9, 10)
    dirac.dirac_moves()

    assert dirac.player2_wins == 121908465540796
    assert dirac.player1_wins == 157595953724471