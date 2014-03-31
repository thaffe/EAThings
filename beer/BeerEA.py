from beer.Beer import Beer
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
        for individual in self.children:
            res = self.beer.run(individual)

            individual.fitness = max(0.01,res[0] - res[1])
            if individual.fitness > self.best_individual.fitness or not self.best_history:
                self.best_history = self.beer.history
