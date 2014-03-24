from copy import deepcopy
from core.EA import *
from Flatland import Flatland
from flatland.FlatlandAgent import FlatlandAgent


class FlatlandEA(EA):

    dynamic = False

    def create_individual(self, genotype=None):
        return FlatlandAgent(genotype)

    def run_fitness_tests(self, individuals):
        if self.dynamic or not self.maps:
            self.maps = []
            for _ in xrange(5):
                self.maps.append(Flatland())

        for individual in individuals:
            if self.dynamic or not individual.maps:
                individual.maps = []
                for map in self.maps:
                    test_map = deepcopy(map)
                    test_map.play(individual)
                    individual.fitness += test_map.food_gathered - 10 * test_map.poisoned
                    if individual.fitness > self.best_individual.fitness:
                        temp = test_map.history
                        test_map = deepcopy(map)
                        test_map.history = temp
                        individual.maps.append(test_map)