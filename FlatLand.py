from random import *
from numpy import array


class Direction:
    def __init__(self):
        d = randint(-1, 1)
        self.val = array([d, 0 if d else randint(-1, 1)])

    def turn_left(self):
        if self.val[0]:
            self.val[1] = self[0]
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
            pass
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

        front_smell = self.map[self.agent_pos + direction]
        front_smell = self.map[self.agent_pos + direction]
        direction.turn_left()
        left_smell = self.map[self.agent_pos + direction]
        right_smell = self.map[self.agent_pos - direction]

        return [front_smell, left_smell, right_smell]


    @property
    def legitimate_position(self):
        return 0 < self.agent_pos[0] < len(self.map) and 0 < self.agent_pos[1] < len(self.map[self.agent_pos[0]])


FlatLand()