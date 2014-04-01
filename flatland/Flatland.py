from random import *
from numpy import array, remainder


class Flatland:
    N = 8
    M = 8
    step_count = 50

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
        self.best_fitness = 0

    def play(self, agent):
        while len(self.history) < self.step_count and self.poisoned < 1:
            self.move(agent.get_move_from_smell(self.smell(), len(self.history)))

    def move(self, move):
        if move == 'f':
            self.agent_pos = tuple(remainder(self.agent_pos + self.agent_direction.val, (len(self.map), len(self.map[0]))))
        elif move == 'l':
            self.agent_direction.turn_left()
            self.agent_pos = tuple(remainder(self.agent_pos + self.agent_direction.val, (len(self.map), len(self.map[0]))))
        elif move == 'r':
            self.agent_direction.turn_right()
            self.agent_pos = tuple(remainder(self.agent_pos + self.agent_direction.val, (len(self.map), len(self.map[0]))))
        elif move == 'n':
            pass
        else:
            raise AttributeError

        if not self.legitimate_position:
            raise AttributeError
        else:
            self.history.append(move)
            if self.map[self.agent_pos] == 'f':
                self.map[self.agent_pos] = '0'
                self.food_gathered += 1
            elif self.map[self.agent_pos] == 'p':
                self.map[self.agent_pos] = '0'
                self.poisoned += 1

    def smell(self):
        direction = self.agent_direction
        front_smell = self.get_cell(self.agent_pos + direction.val)
        direction.turn_left()
        left_smell = self.get_cell(self.agent_pos + direction.val)
        right_smell = self.get_cell(self.agent_pos - direction.val)
        direction.turn_right()

        return [front_smell, left_smell, right_smell]

    def get_cell(self, pos):
        return self.map[pos[0] % self.N][pos[1] % self.M]

    @property
    def legitimate_position(self):
        return 0 <= self.agent_pos[0] < len(self.map) and 0 <= self.agent_pos[1] < len(self.map[self.agent_pos[0]])


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
