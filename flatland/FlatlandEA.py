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

    def create_individual(self, genotype=None):
        return FlatlandAgent(self.mutation_rate, genotype)

    def run_fitness_tests(self):
        if self.dynamic or not self.maps:
            self.old_maps.append(self.maps)
            self.maps = [Flatland() for _ in xrange(5)]

        individuals = self.children if not self.dynamic else self.children + self.adults
        for individual in individuals:
            print "lol", len(self.children)
            temp_hist = []
            temp_food_gathered = []
            temp_poisoned = []
            for map in self.maps:
                test_map = deepcopy(map)
                test_map.play(individual)
                temp_hist.append(test_map.history)
                temp_food_gathered.append(test_map.food_gathered)
                temp_poisoned.append(test_map.poisoned)
                map_fitness = test_map.food_gathered - test_map.poisoned
                individual.fitness += map_fitness
                if map_fitness > map.best_fitness:
                    map.best_solution = test_map.history
                    map.food_gathered_by_best = test_map.food_gathered
                    map.poisoned_by_best = test_map.poisoned

            individual.fitness = max(individual.fitness, 0)
            if individual.fitness > self.best_individual.fitness:
                for i in xrange(len(self.maps)):
                    self.maps[i].history = temp_hist[i]
                    self.maps[i].food_gathered = temp_food_gathered[i]
                    self.maps[i].poisoned = temp_poisoned[i]
