from random import *
from math import exp
from BeerStates import BeerStates


class Beer:

    Width = 30
    Height = 15
    AgentSize = 5

    def __init__(self, random=True):
        self.tests = [BeerTest() for _ in xrange(40)]

    def shadows(self):
        return [self.object_pos <= self.agent_pos + i < self.object_pos + self.object_size for i in xrange(self.AgentSize)]

    def timestep(self, step):
        
        self.agent_pos = (self.agent_pos + self.agent.getmove(self.shadows(), step)) % self.Width
        self.object_pos = (self.object_pos + self.vx) % self.Width
        self.history.save_pos(self.object_pos, self.agent_pos)

    def runTest(self, test):
        self.shadow_sum = 0
        self.agent_pos = test.agent_pos
        self.object_pos = test.object_pos
        self.object_size = test.object_size
        self.vx = test.vx

        for step in xrange(0, 15):
            self.timestep(step)
            # if step < 11 or self.object_size < 5:
            #     self.total += self.shadows().count(True) / 30
            # else:
            #     self.total -= self.shadows().count(True) / 30
        res = 0
        self.total += 1/(1+(abs((self.agent_pos + self.AgentSize/2.0) - (self.object_pos + self.object_size/2.0)))**0.33)
        # self.total -= self.shadows().count(True)

        if self.object_size <= 4:
            if self.object_pos >= self.agent_pos and self.object_pos + self.object_size <= self.agent_pos + self.AgentSize:
                self.catches += 1
                res = 1
                self.total -= max(self.agent_pos - self.object_pos, 0) + max((self.object_pos + self.object_size) - (self.agent_pos + self.AgentSize), 0)
        else:
            if not (self.agent_pos + self.AgentSize <= self.object_pos or self.agent_pos >= self.object_pos + self.object_size):
                self.crashes += 1
                res = -1
                self.total += 3 * (max(self.agent_pos - (self.object_pos + self.object_size), 0) + max(self.object_pos - (self.agent_pos + self.AgentSize), 0))

        self.history.save_state(self.object_size, res)
        self.total += res

    def run(self, agent):
        self.total = 60
        self.catches = 0
        self.crashes = 0
        self.agent = agent
        self.history = BeerStates()
        for test in self.tests:
            self.runTest(test)

        return self.total


class BeerTest:

    def __init__(self, object_size=0):
        self.object_size = randint(1, 6) if not object_size else object_size
        self.object_pos = randint(0, Beer.Width - self.object_size)
        self.agent_pos = randint(0, Beer.Width - Beer.AgentSize)
        self.vx = 0