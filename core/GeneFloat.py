from random import random
import math

from core.Gene import Gene


class GeneFloat(Gene):

    def mutate(self, mutation_rate):
        sign = 1 if random() > 0.5 else -1
        if self.source.logarithmic:
            self.value = min(max(self.value + (self.source.max - self.source.min) * sign * mutation_rate.next(), self.source.min), self.source.max)
        else:
            self.value = min(max(self.value + (self.source.max - self.source.min) * sign * mutation_rate.next(), self.source.min), self.source.max)

    def compare(self, other):
        return abs(self.value - other.value) / (self.source.max - self.source.min)

    def random_value(self, source):
        self.source = source
        if source.logarithmic:
            self.value = math.exp(source.ln_min + (source.ln_max - source.ln_min) * random())
        else:
            self.value = source.min + (source.max - source.min) * random()


class GeneFloatSource():

    def __init__(self, min, max, logarithmic):
        self.min = min
        self.max = max
        self.logarithmic = logarithmic
        if logarithmic:
            self.ln_min = math.log(min)
            self.ln_max = math.log(max)