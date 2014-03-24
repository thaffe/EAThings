from random import *


class NormDist():

    def __init__(self, mu, sigma, min=0.0, max=1.0):
        self.mu = mu
        self.sigma = sigma
        self.min = min
        self.max = max

    def next(self):
        value = normalvariate(self.mu, self.sigma)
        while not self.min < value < self.max:
            value = normalvariate(self.mu, self.sigma)
        return value