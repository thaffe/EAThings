from random import *
from abc import *
import sys

import Strategies
from core.NormDist import NormDist


class EA():
    parent_pool_size = 60
    adult_pool_size = 100
    child_pool_size = 100
    adult_selection_mode = Strategies.GENERATION_REPLACEMENT
    number_of_parents = 2
    crossover_rate = NormDist(2, 5, 1, 20)
    mutation_rate = NormDist(0.01, 0.1, 0.0, 0.5)
    max_generations = 100

    sd = 0
    mean = 0

    def __init__(self, fitness_goal=0):
        self.parent_selection_strategy = Strategies.fitness
        self.fitness_goal = fitness_goal
        self.means = []
        self.sds = []
        self.bests = []
        self.best_individual = None
        self.current_generation = 0

    def set_parent_strategy(self, strategy):
        self.parent_selection_strategy = strategy

    @abstractmethod
    def create_individual(self, genotype=None):
        pass

    def run(self, plot=False):
        self.children = [self.create_individual() for _ in xrange(self.adult_pool_size)]
        self.adults = None
        self.current_generation = 0
        self.update_stats()
        print("Starting Evolution")
        while self.current_generation < self.max_generations and (not self.fitness_goal or self.fitness_goal > self.best_individual.fitness):
            sys.stdout.write(
                "\r Generation:%d/%d BestFittness:%f ... Testing fitness" % (
                self.current_generation, self.max_generations, self.best_individual.fitness))
            sys.stdout.flush()
            self.run_fitness_tests()
            sys.stdout.write(
                "\r Generation:%d/%d BestFittness:%f ... Adult selection" % (
                self.current_generation, self.max_generations, self.best_individual.fitness))
            sys.stdout.flush()
            adults = self.parent_selection(
                self.adult_selection()
            )
            sys.stdout.write(
                "\r Generation:%d/%d BestFittness:%f ... Reproduction" % (
                self.current_generation, self.max_generations, self.best_individual.fitness))
            sys.stdout.flush()
            self.children = self.reproduction(adults)

            self.current_generation += 1

        print(self.best_individual)
        if plot:
            self.plot()

    def parent_selection(self, individuals):
        self.update_stats()
        exp_sum = self.parent_selection_strategy(self, individuals)

        #if parent selection strategy returns list then no need to spin roulette wheel
        if isinstance(exp_sum, list): return exp_sum

        return [x for x in roulette(individuals, self.parent_pool_size, exp_sum)]

    def adult_selection(self):
        if self.adult_selection_mode == Strategies.GENERATION_REPLACEMENT or parents is None:
            #over producion
            return self.get_best(self.children, self.adult_pool_size)
        else:
            #generation mixing
            return self.get_best(self.adults + self.children, self.adult_pool_size)

    def reproduction(self, individuals):
        childpool = []
        gene_count = individuals[0].gene_count
        iter = cycle_random(individuals)
        #iterate to the childpool is filled up
        while len(childpool) < self.child_pool_size:
            # TODO: Drive roulette? (Inkludere expval)
            current_parents = [iter.next() for _ in xrange(self.number_of_parents)]
            #initiates empty genotypes for the children

            genotypes = [[] for _ in xrange(self.number_of_parents)]
            parent_index = 0
            prev_crossover = 0
            next_crossover = int(self.crossover_rate.next()*gene_count)
            while prev_crossover < gene_count:
                for j in xrange(self.number_of_parents):
                    for i in xrange(prev_crossover, min(next_crossover, gene_count)):
                        genotypes[j].append((current_parents[(parent_index+j) %
                                                             self.number_of_parents].get_child_gene(i)))
                parent_index = (parent_index + 1) % self.number_of_parents
                prev_crossover = next_crossover
                next_crossover += max(int(self.crossover_rate.next()*gene_count), 1)

            #Initiate the children
            for genotype in genotypes:
                childpool.append(self.create_individual(genotype))
                if len(childpool) == self.child_pool_size:
                    return childpool

        return childpool

    def get_best(self, individuals, size):
        return sorted(individuals, lambda x, y: cmp(y.fitness, x.fitness))[:size]

    def update_stats(self):
        individuals = self.children if not self.adults else self.children + self.adults
        self.mean = 0
        best = individuals[0]
        for i in individuals:
            self.mean += i.fitness
            if i.fitness > best.fitness:
                best = i

        if not self.best_individual or self.best_individual.fitness < best.fitness:
            self.best_individual = best

        self.mean /= (len(individuals) * 1.0)
        self.sd = (sum((i.fitness - self.mean) ** 2 for i in individuals) / len(individuals)) ** 0.5

        self.bests.append(best.fitness)
        self.means.append(self.mean)
        self.sds.append(self.sd)

    def run_fitness_tests(self):
        for child in self.children:
            child.calculate_fitness()


def roulette(individuals, n, total):
    i = 0
    w, v = individuals[0].exp_val, individuals[0]
    while n:
        x = total * (1 - random() ** (1.0 / n))
        total -= x
        while x > w:
            x -= w
            i = min(len(individuals) - 1, i + 1)
            w, v = individuals[i].exp_val, individuals[i]
        w -= x
        yield v
        n -= 1


def cycle_random(iterable):
    saved = []
    for element in iterable:
        yield element
        saved.append(element)
    while saved:
        shuffle(saved)
        for element in saved:
            yield element