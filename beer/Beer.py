from random import *
from math import exp, floor
from BeerStates import BeerStates


class Beer:

    Width = 30
    Height = 15
    AgentSize = 5
    avoid_objects = True
    def __init__(self, random=True):
        self.total = 0
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

        # big_catch = not (self.agent_pos + self.AgentSize <= self.object_pos or self.agent_pos >= self.object_pos + self.object_size)
        # small_catch =not big_catch and self.object_pos >= self.agent_pos and self.object_pos + self.object_size <= self.agent_pos + self.AgentSize
        big_catch = self.object_size >= 5 and sum(self.shadow_array) > 0
        small_catch = not big_catch and sum(self.shadow_array) == self.object_size
        res = 0
        if Beer.avoid_objects:
            if self.object_size <= 4:
                # self.total += 1/(1+(abs((self.agent_pos + self.AgentSize/2.0) - (self.object_pos + self.object_size/2.0)))**0.5)
                if small_catch:
                    res = 1
            elif big_catch:
                res = -1
            else:
                self.total += 2

            res = 1 if small_catch else -1 if big_catch else 0
        else:
            # self.total += 1/(1+(abs((self.agent_pos + self.AgentSize/2.0) - (self.object_pos + self.object_size/2.0)))**0.5)
            res = 1 if big_catch or small_catch else 0

        self.total += res
        self.history.save_state(self.object_size, res)

    def run(self, agent):
        self.total = 0
        self.agent = agent
        self.history = BeerStates()
        for test in self.tests:
            self.runTest(test)

        # while i < len(self.tests)*(2.0/3.0):
        #     self.runTest(self.tests[i])
        #     i += 1
        # if self.total > len(self.tests)*(2.0/3.0)*0.8:
        #     temp = self.total
        #     while i < len(self.tests):
        #         self.runTest(self.tests[i])
        #         i += 1
        #     self.total = max(self.total, temp)

        return self.total


class BeerTest:

    def __init__(self, object_size=0):
        self.object_size = randint(1, 6) if not object_size else object_size
        self.object_pos = randint(0, Beer.Width - self.object_size)
        self.agent_pos = randint(0, Beer.Width - Beer.AgentSize)
        self.vx = 1