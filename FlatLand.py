from random import *
from numpy import array


class Direction:
    def __init__(self):
        d = randint(-1, 1)
        self.val = array([d, 0 if d else 1 if random() < 0.5 else -1])

    def turn_left(self):
        if self.val[0]:
            self.val[1] = self.val[0]
            self.val[0] = 0
        else:
            self.val[0] = -self.val[1]
            self.val[1] = 0

    def turn_right(self):
        if self.val[0]:
            self.val[1] = -self.val[0]
            self.val[0] = 0
        else:
            self.val[0] = self.val[1]
            self.val[1] = 0


class FlatLand:
    N = 8
    M = 8
    def __init__(self, N=8, M=8, f=0.5, p=0.5):
        self.map = array([
            ['f' if random() < f else 'p' if random() < p else 0 for _ in xrange(M)] for _ in xrange(N)
        ])
        while True:
            self.agent_pos = (randint(0, N - 1), randint(0, M - 1))
            if self.map[self.agent_pos] == '0': break;
        self.agent_direction = Direction()
        self.food_gathered = 0
        self.poisoned = 0
        self.history = []

    def move(self, move):
        if move == 'f':
            self.agent_pos += self.agent_direction.val
        elif move == 'l':
            self.agent_direction.turn_left()
            self.agent_pos += self.agent_direction.val
        elif move == 'r':
            self.agent_direction.turn_right()
            self.agent_pos += self.agent_direction.val
        elif move == 'n':
            self.history.append(None)
        else:
            raise AttributeError

        if not self.legitimate_position:
            self.agent_pos -= self.agent_direction.val
            return False
        elif self.map[self.agent_pos] == 'f':
            self.map[self.agent_pos] = None
            self.food_gathered += 1
        elif self.map[self.agent_pos] == 'p':
            self.poisoned += 1

        return True

    def smell(self):
        direction = self.agent_direction
        print(self.agent_pos, direction.val,tuple(self.agent_pos + direction.val))
        front_smell = self.get_cell(self.agent_pos + direction.val)
        direction.turn_left()
        left_smell = self.get_cell(self.agent_pos + direction.val)
        right_smell = self.get_cell(self.agent_pos - direction.val)

        return [front_smell, left_smell, right_smell]

    def get_cell(self, pos):
        return 0 if pos[0] >= self.M or pos[0] < 0 or pos[1] >= self.N or pos[1] < 0 else self.map[tuple(pos)]

    @property
    def legitimate_position(self):
        return 0 < self.agent_pos[0] < len(self.map) and 0 < self.agent_pos[1] < len(self.map[self.agent_pos[0]])


FlatLand()
