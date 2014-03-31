from random import *
from BeerStates import BeerStates


class Beer:

    Width = 30
    Height = 15
    AgentSize = 5

    def __init__(self, random=True):
        self.tests = [BeerTest() for _ in xrange(40)]

    def shadows(self):
        return [self.object_pos <= self.agent_pos + i <= self.object_pos + self.object_size for i in xrange(self.AgentSize)]

    def timestep(self, step):
        self.agent_pos = max(min(self.agent_pos + int(self.agent.getmove(self.shadows(), step)*4), self.Width - self.AgentSize), 0)
        self.object_pos += self.vx
        if self.object_pos + self.object_size >= self.Width:
            self.object_pos -= 2 * (self.object_pos + self.object_size - self.Width)
            self.vx *= -1
        elif self.object_pos <= 0:
            self.object_pos *= -1
            self.vx *= -1
        self.history.save_pos(self.object_pos, self.agent_pos)

    def runTest(self, test):
        self.agent_pos = test.agent_pos
        self.object_pos = test.object_pos
        self.object_size = test.object_size
        self.vx = test.vx

        for step in xrange(0, 15):
            self.timestep(step)
        res = 0
        if self.object_size < 5:
            if self.agent_pos <= self.object_pos <= self.agent_pos + self.AgentSize - self.object_size:
                self.catches += 1
                res = 1
        elif (self.agent_pos - self.object_size) < self.object_pos < self.agent_pos + self.AgentSize + self.object_size:
            self.crashes += 1
            res = -1
        self.history.save_state(self.object_size, res)

    def run(self, agent):
        self.catches = 0
        self.crashes = 0
        self.agent = agent
        self.history = BeerStates()
        for test in self.tests:
            self.runTest(test)

        return self.catches, self.crashes


class BeerTest:

    def __init__(self):
        self.object_size = randint(1, 6)
        self.object_pos = randint(0, Beer.Width - self.object_size)
        self.agent_pos = randint(0, Beer.Width - Beer.AgentSize)
        self.vx = 0 #1 if random() > 0.5 else -1