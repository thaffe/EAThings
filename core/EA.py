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
    parent_selection_strategy = None
    crossover_rate = NormDist(2, 5, 1, 20)
    mutation_rate = NormDist(0.3, 0.1, 0.0, 0.5)
    max_generations = 100

    sd = 0
    mean = 0

    def __init__(self, fitness_goal=0):
        self.similarity_weight = 0
        self.fitness_goal = fitness_goal
        self.means = []
        self.sds = []
        self.bests = []
        self.best_similarities = [0]
        self.best_individual = None
        self.current_generation = 0

        self.adults = None
        self.children = None

    @abstractmethod
    def create_individual(self, genotype=None):
        pass

    def run(self):
        self.children = [self.create_individual() for _ in xrange(self.child_pool_size)]
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
                "\r Generation:%d/%d  BestFittness:%f ... Adult selection" % (
                self.current_generation, self.max_generations, self.best_individual.fitness))
            sys.stdout.flush()
            self.adult_selection()
            self.parent_selection()
            sys.stdout.write(
                "\r Generation:%d/%d BestFittness:%f ... Reproduction" % (
                self.current_generation, self.max_generations, self.best_individual.fitness))
            sys.stdout.flush()
            self.children = self.reproduction(self.adults)

            self.current_generation += 1

        print(self.best_individual)
        
        self.run_finals()

    def parent_selection(self):
        exp_sum = EA.parent_selection_strategy(self, self.adults)

        #if parent selection strategy returns list then no need to spin roulette wheel
        if isinstance(exp_sum, list): return exp_sum

        return [x for x in roulette(self.adults, self.parent_pool_size, exp_sum)]

    def adult_selection(self):
        if self.adult_selection_mode == Strategies.GENERATION_REPLACEMENT or self.adults is None:
            #over producion
            individuals = self.sort(self.children)
        else:
            #generation mixing
            individuals = self.sort(self.adults + self.children)

        self.update_stats()
        self.adults = individuals[:self.adult_pool_size]

    def reproduction(self, individuals):
        childpool = []
        gene_count = individuals[0].gene_count
        iter = cycle_random(individuals)
        #iterate to the childpool is filled up
        while len(childpool) < self.child_pool_size:
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

    def sort(self, individuals):
        return sorted(individuals, lambda x, y: cmp(y.fitness, x.fitness))

    def update_stats(self):
        individuals = self.children if not self.adults else self.children + self.adults
        self.mean = 0
        best = individuals[0]
        for i in individuals:
            self.mean += i.fitness
            if i.fitness > best.fitness:
                best = i

        if self.best_individual:
            self.best_similarities.append(self.best_individual.compare(best) * 100)
        if not self.best_individual or self.best_individual.fitness < best.fitness:
            self.best_individual = best

        self.mean /= (len(individuals) * 1.0)
        self.sd = (sum((i.fitness - self.mean) ** 2 for i in individuals) / len(individuals)) ** 0.5

        if self.similarity_weight > 0:
            for i in xrange(self.adult_pool_size):
                self.similarity_mean = 0
                min_similarity = 0
                for individual in individuals:
                    if individual != individuals[i]:
                        individual.similarity = individual.compare(individuals[i])
                        min_similarity = min(min_similarity, individual.similarity)
                        self.similarity_mean += individual.similarity
                individuals[i].similarity = min_similarity
                self.similarity_mean += min_similarity
                self.similarity_mean /= len(individuals)
                self.similarity_sd = (sum((i.similarity - self.similarity_mean) ** 2 for i in individuals) / len(individuals)) ** 0.5

                for individual in individuals:
                    individual.fitness += (self.similarity_mean - individual.similarity) / self.similarity_sd * \
                                          self.sd * self.similarity_weight / self.adult_pool_size

                individuals = individuals[0:i + 1] + self.sort(individuals[i + 1:])

        self.bests.append(best.fitness)
        self.means.append(self.mean)
        self.sds.append(self.sd)

    def run_fitness_tests(self):
        for child in self.children:
            child.calculate_fitness()

    def run_finals(self):
        pass


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