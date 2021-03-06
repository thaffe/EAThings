from beer.Beer import *
from beer.BeerAgent import BeerAgent
from core.EA import EA


class BeerEA(EA):

    def __init__(self):
        EA.__init__(self)
        self.beer = Beer()
        self.best_history = None
        self.tests = 40
        self.beer.tests = [BeerTest(1 + int(floor(i/(self.tests/6.0)))) for i in xrange(self.tests)]

    def create_individual(self, genotype=None):
        return BeerAgent(self.mutation_rate, genotype)

    def run_fitness_tests(self):
        individuals = self.children #if not self.adults else self.children + self.adults
        for individual in individuals:
            individual.fitness = max(0.001, self.beer.run(individual))
            if individual.fitness > self.best_individual.fitness or not self.best_history:
                self.best_history = self.beer.history

    def run_finals(self):
        self.best_individual.do_tests_on_ann()
