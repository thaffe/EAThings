from random import *


class NormDist():

    def __init__(self, mu, sigma, min=0.0, max=1.0, clamp=True):
        self.mu = mu
        self.sigma = sigma
        self.min = min
        self.max = max
        self.clamp = clamp

    def next(self):
        value = normalvariate(self.mu, self.sigma)
        if self.clamp:
            return min(max(value, self.min), self.max)
        while not self.min < value < self.max:
            value = normalvariate(self.mu, self.sigma)
        return value