from copy import deepcopy
from core.EA import *
from Flatland import Flatland
from flatland.FlatlandAgent import FlatlandAgent


class FlatlandEA(EA):

    dynamic = False

    def __init__(self, fitness_goal=0):
        EA.__init__(self, fitness_goal=0)
        self.maps = [Flatland() for _ in xrange(5)]
        self.old_maps = []
        self.best_maps = deepcopy(self.maps)

    def create_individual(self, genotype=None):
        return FlatlandAgent(self.mutation_rate, genotype)

    def run_fitness_tests(self):
        if self.dynamic or not self.maps:
            self.old_maps.append(self.maps)
            self.maps = [Flatland() for _ in xrange(5)]
            self.old_maps = deepcopy(self.maps)

        individuals = self.children if not self.dynamic or not self.adults else self.children + self.adults
        for individual in individuals:
            individual.fitness = 0
            temp_maps = []
            for map in self.maps:
                test_map = deepcopy(map)
                temp_maps.append(test_map)
                test_map.play(individual)
                map_fitness = test_map.food_gathered - test_map.poisoned
                individual.fitness += map_fitness

                if map_fitness > map.best_fitness:
                    map.best_solution = test_map.history
                    map.food_gathered_by_best = test_map.food_gathered
                    map.poisoned_by_best = test_map.poisoned

            individual.fitness = max(individual.fitness, 0.01)
            # print individual.fitness
            if individual.fitness > self.best_individual.fitness:
                if self.dynamic:
                    self.best_maps = self.old_maps
                for i in xrange(len(self.maps)):
                    self.best_maps[i].history = temp_maps[i].history
                    self.best_maps[i].food_gathered = temp_maps[i].food_gathered
                    self.best_maps[i].poisoned = temp_maps[i].poisoned
