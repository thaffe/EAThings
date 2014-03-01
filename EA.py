from random import *
from abc import *
import sys
import Strategies


class EA():
    parent_pool_size = 60
    adult_pool_size = 100
    child_pool_size = 100
    adult_selection_mode = Strategies.GENERATION_REPLACEMENT
    number_of_parents = 2
    crossover_rate = 0.2
    max_generations = 100

    sd = 0
    mean = 0

    def __init__(self, fitness_goal):
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
        children = [self.create_individual() for _ in xrange(self.adult_pool_size)]
        adults = None
        self.current_generation = 0
        self.update_stats(children)
        print("Starting Evolution")
        while self.current_generation < self.max_generations and self.fitness_goal > self.best_individual.fitness:
            sys.stdout.write(
                "\r Generation:%d/%d BestFittness:%f" % (
                self.current_generation, self.max_generations, self.best_individual.fitness))
            sys.stdout.flush()
            adults = self.parent_selection(
                self.adult_selection(adults, children)
            )
            children = self.reproduction(adults)

            self.current_generation += 1

        print(self.best_individual)
        if plot: self.plot()
        # self.plot()

    def parent_selection(self, individuals):
        self.update_stats(individuals)
        exp_sum = self.parent_selection_strategy(self, individuals)

        #if parent selection strategy returns list then no need to spin roulette wheel
        if isinstance(exp_sum, list): return exp_sum

        return [x for x in roulette(individuals, self.parent_pool_size, exp_sum)]
        #Simple, slow roulette wheel
        # parents = []
        # ticket = uniform(0, exp_sum)
        # for i in cycle(range(len(individuals))):
        #     #while len(parents) < self.parent_pool_size:
        #     individual = individuals[i]
        #     ticket -= individual.exp_val
        #     if ticket <= 0:
        #         ticket = uniform(0, exp_sum)
        #         parents.append(individual)
        #         if len(parents) == self.parent_pool_size: break
        #
        # return parents

    def adult_selection(self, parents, children):
        if self.adult_selection_mode == Strategies.GENERATION_REPLACEMENT or parents is None:
            #over producion
            return self.get_best(children, self.adult_pool_size)
        else:
            #generation mixing
            return self.get_best(parents + children, self.adult_pool_size)

    def reproduction(self, individuals):
        children = []
        gens = individuals[0].number_of_gens
        iter = cycle_random(individuals)
        #iterate to the childpool is filled up
        while len(children) < self.child_pool_size:
            current_parents = [iter.next() for _ in xrange(self.number_of_parents)]
            #initiates empty genotypes for the children
            genotypes = [x[:] for x in [[0] * Individual.number_of_gens] * self.number_of_parents]
            #Loop over parens gens to map them to the children
            for bit in xrange(gens):
                if random() < self.crossover_rate:
                    current_parents = current_parents[-1:] + current_parents[:-1]

                for i in xrange(self.number_of_parents):
                    genotypes[i][bit] = current_parents[i].get_child_gen(bit)
            #Initiate the children
            for gen in genotypes:
                children.append(self.create_individual(gen))
                if len(children) == self.child_pool_size: return children

        return children

    def get_best(self, individuals, size):
        return sorted(individuals, lambda x, y: cmp(y.fitness, x.fitness))[:size]

    def update_stats(self, individuals):
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


class Individual():
    fitness = 0
    exp_val = 0
    number_of_gens = 40
    number_of_gene_symbols = 2
    mutation_rate = 0.01
    phenotype = None

    def __init__(self, genotype=None):
        self.genotype = genotype if not genotype is None else self.get_random_genotype()
        # self.mutate()
        self.phenotype = self.generate_phenotype()
        self.fitness = self.calculate_fitness()

    def __repr__(self):
        return "{Fitness:%f  exp:%f gen:%s}\n" % (self.fitness, self.exp_val, "".join(str(x) for x in self.genotype))

    def get_child_gen(self, gen_index):
        return self.genotype[gen_index] if random() > self.mutation_rate else randint(0,
                                                                                      self.number_of_gene_symbols - 1)

    def mutate(self):
        for i in xrange(self.number_of_gens):
            if random() < self.mutation_rate:
                self.genotype[i] = randint(0, self.number_of_gene_symbols - 1)

    def get_random_genotype(self):
        return [randint(0, self.number_of_gene_symbols - 1) for _ in xrange(self.number_of_gens)]

    @abstractmethod
    def generate_phenotype(self):
        pass

    @abstractmethod
    def calculate_fitness(self):
        pass

    @abstractmethod
    def phenotype_str(self):
        pass

    #Super fast roulette runs at O(n+individuals)
    #used to iterate forever over a list, shuffeling the list every time the list is iterated one time
    #It is based on the following algorithm:
    #def n_random_numbers_decreasing(v, n):
    #   """Like reversed(sorted(v * random() for i in range(n))),
    #   but faster because we avoid sorting."""
    #   while n:
    #       v *= random.random() ** (1.0 / n)
    #       yield v
    #       n -= 1

#The function weighted_sample is just this algorithm fused with a walk of the items list to pick out the items selected by those random numbers.
#This in turn works because the probability that n random numbers 0..v will all happen to be less than z is P = (z/v)n.
#  Solve for z, and you get z = vP1/n.
# Substituting a random number for P picks the largest number with the correct distribution; and we can just repeat the process to select all the other numbers.
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