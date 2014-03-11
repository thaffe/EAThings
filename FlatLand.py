from random import *
from numpy import array


class Direction(array):

    def __init__(self):
        self.append(randint(-1, 1))
        self.append(0 if self[0] else randint(-1, 1))

    def turn_left(self):
        if self[0]:
            self[1] = self[0]
            self[0] = 0
        else:
            self[0] = -self[1]
            self[1] = 0

    def turn_right(self):
        if self[0]:
            self[1] = -self[0]
            self[0] = 0
        else:
            self[0] = self[1]
            self[1] = 0


class FlatLand:

    def __init__(self, N=8, M=8, f=0.5, p=0.5):
        self.map = array([
            ['f' if random() < f else 'p' if random() < p else None for _ in xrange(M)] for _ in xrange(N)
        ])

        legitimate_start_position = False
        while not legitimate_start_position:
            self.agent_pos = array([randint(0, N - 1), randint(0, M - 1)])
            if not self.map[self.agent_pos]:
                legitimate_start_position = True

        self.agent_direction = Direction()

        self.food_gathered = 0
        self.poisoned = 0
        self.history = []

    def move(self, move):
        if move == 'f':
            self.agent_pos += self.agent_direction
            self.history.append(self.agent_direction)
        elif move == 'l':
            self.agent_direction.turn_left()
            self.agent_pos += self.agent_direction
            self.history.append(self.agent_direction)
        elif move == 'r':
            self.agent_direction.turn_right()
            self.agent_pos += self.agent_direction
            self.history.append(self.agent_direction)
        elif move == 'n':
            self.history.append(None)
        else:
            raise AttributeError

        if not self.legitimate_position:
            self.agent_pos -= self.agent_direction
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
        direction.turn_left()
        left_smell = self.map[self.agent_pos + direction]
        right_smell = self.map[self.agent_pos - direction]

        return [front_smell, left_smell, right_smell]


    @property
    def legitimate_position(self):
        return  0 < self.agent_pos[0] < len(self.map) and 0 < self.agent_pos[1] < len(self.map[self.agent_pos[0]])