from random import *
from math import exp, floor
from BeerStates import BeerStates


class Beer:

    Width = 30
    Height = 15
    AgentSize = 5
    avoid_objects = True
    def __init__(self, random=True):
        self.fitness = 0
        self.object_size = None
        self.object_start = None
        self.object_end = None
        self.agent_start = None
        self.agent_end = None
        self.shadow_array = None
        self.tests = [BeerTest(1 + floor(i/16.66)) for i in xrange(100)]


    def shadows(self):
        if self.object_start < self.object_end:
            return [self.object_start <= (self.agent_start + i)%Beer.Width < self.object_end for i in xrange(self.AgentSize)]

        return [(self.agent_start+i) % Beer.Width >= self.object_start
                or (self.agent_start+i) % Beer.Width < self.object_end
                for i in xrange(self.AgentSize)]




    def timestep(self, step):
        self.shadow_array = self.shadows()
        self.agent_start = (self.agent_start + self.agent.getmove(self.shadow_array, step)) % Beer.Width
        self.agent_end = (self.agent_start + Beer.AgentSize) % Beer.Width
        self.object_start = (self.object_start + self.vx) % Beer.Width
        self.object_end = (self.object_start + self.object_size) % Beer.Width

        self.history.save_pos(self.object_start, self.agent_start)

    def runTest(self, test):
        self.object_size = test.object_size
        self.agent_start = test.agent_pos
        self.agent_end = (test.agent_pos+Beer.AgentSize) % Beer.Width
        self.object_start = test.object_pos
        self.object_end = (test.object_pos + test.object_size) % Beer.Width
        self.vx = test.vx

        for step in xrange(0, Beer.Height):
            self.timestep(step)

        big_catch = self.object_size >= 5 and sum(self.shadow_array) > 0
        small_catch = not big_catch and sum(self.shadow_array) == self.object_size
        res = 0
        if Beer.avoid_objects:
            if self.object_size <= 4:
                self.fitness += 0.5 * (1 - (min(
                    abs((self.agent_start + self.AgentSize/2.0) - (self.object_start + self.object_size/2.0)),
                    abs((self.agent_end - self.AgentSize/2.0) - (self.object_start + self.object_size/2.0))
                ) / (self.Width/2))**2)
                if small_catch:
                    res = 1
            elif big_catch:
                res = -1
            else:
                self.fitness += 1

        else:
            self.fitness += 1 - (min(
                abs((self.agent_start + self.AgentSize/2.0) - (self.object_start + self.object_size/2.0)),
                abs((self.agent_end - self.AgentSize/2.0) - (self.object_start + self.object_size/2.0))
            ) / (self.Width/2))**2
            res = 1 if big_catch or small_catch else 0

        self.fitness += res * 0.5
        self.history.save_state(self.object_size, res)

    def run(self, agent):
        self.fitness = 0
        self.agent = agent
        self.history = BeerStates()
        for test in self.tests:
            self.runTest(test)

        # i = 0
        # while i < len(self.tests)*(1.0/3.0):
        #     self.runTest(self.tests[len(self.tests) - i - 1])
        #     i += 1
        # if self.fitness > len(self.tests)*(1.0/3.0)*0.7:
        #     temp = self.fitness
        #     i = 0
        #     while i < len(self.tests)*(2.0/3.0):
        #         self.runTest(self.tests[i])
        #         i += 1
        #     self.fitness = max(self.fitness, temp)

        return self.fitness / 40 * 100


class BeerTest:

    def __init__(self, object_size=0):
        self.object_size = randint(1, 6) if not object_size else object_size
        self.object_pos = randint(0, Beer.Width - self.object_size)
        self.agent_pos = randint(0, Beer.Width - Beer.AgentSize)
        self.vx = 1