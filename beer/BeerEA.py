from math import floor
from beer.Beer import *
from beer.BeerAgent import BeerAgent
from core.EA import EA


class BeerEA(EA):

    def __init__(self):
        EA.__init__(self)
        self.beer = Beer()
        self.best_history = None

    def create_individual(self, genotype=None):
        return BeerAgent(genotype)

    def run_fitness_tests(self):
        self.beer.tests = [BeerTest(1 + floor(i/7)) for i in xrange(40)]

        for individual in self.children:
            individual.fitness = self.beer.run(individual)
            if individual.fitness > self.best_individual.fitness or not self.best_history:
                self.best_history = self.beer.history
