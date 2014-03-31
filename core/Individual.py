from abc import abstractmethod
from copy import deepcopy

from core.NormDist import NormDist


class Individual():

    def __init__(self, mutation_rate, genotype=None):
        self.fitness = 0
        self.exp_val = 0
        self.gene_count = 0
        self.mutation_rate = mutation_rate

        if genotype:
            self.genotype = genotype
            for gene in self.genotype:
                gene.mutate(self.mutation_rate)
        else:
            self.random_genotype()

        for _ in self.genotype:
            self.gene_count += 1

        self.generate_phenotype()

    def __repr__(self):
        return "{Fitness:%f  exp:%f gen:%s}\n" % (self.fitness, self.exp_val, "".join(str(x) for x in self.genotype))

    def get_child_gene(self, gene_index):
        return deepcopy(self.genotype[gene_index])

    def mutate(self):
        for i in xrange(self.gene_count):
            self.genotype[i].mutate(self.mutation_rate)

    def compare(self, other):
        diff = 0
        for i in xrange(len(self.genotype)):
            diff += self.genotype[i].compare(other.genotype[i])
        diff /= len(self.genotype)
        return diff

    @abstractmethod
    def random_genotype(self):
        raise NotImplementedError
        pass

    @abstractmethod
    def calculate_fitness(self):
        raise NotImplementedError
        pass

    @abstractmethod
    def generate_phenotype(self):
        pass

    @abstractmethod
    def phenotype_str(self):
        pass