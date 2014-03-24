from abc import abstractmethod
from copy import deepcopy

from core.NormDist import NormDist


class Individual():
    mutation_rate = NormDist(0.01, 0.1, 0, 1)

    def __init__(self, genotype=None):
        self.fitness = 0
        self.exp_val = 0
        self.gene_count = 0

        if genotype:
            self.genotype = genotype
            for gene in self.genotype:
                gene.mutate(self.mutation_rate)
        else:
            self.random_genotype()

        for _ in self.genotype:
            self.gene_count += 1

        self.phenotype = self.generate_phenotype()

    def __repr__(self):
        return "{Fitness:%f  exp:%f gen:%s}\n" % (self.fitness, self.exp_val, "".join(str(x) for x in self.genotype))

    def get_child_gene(self, gene_index):
        return deepcopy(self.genotype[gene_index])

    def mutate(self):
        for i in xrange(self.number_of_genes):
            self.genotype[i].mutate(self.mutation_rate)

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