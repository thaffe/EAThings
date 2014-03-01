from EA import *


class SurprisingSequence(EA):
    def __init__(self, symbol_length, global_sequence=True):
        EA.__init__(self, 3*symbol_length if global_sequence else 1+symbol_length**2)
        #Settings number of genes in genotype to be 3*symbols for global and 1+symbols^2 for local
        Individual.number_of_gens = self.fitness_goal
        #Number of symbols for gens is symbols length +1 because of the alleles
        Individual.number_of_gene_symbols = symbol_length + 1
        SurprisingSequenceIndividual.global_sequence = global_sequence

    def create_individual(self, genotype=None):
        return SurprisingSequenceIndividual(genotype)


class SurprisingSequenceIndividual(Individual):
    match = 0
    global_sequence = True

    def generate_phenotype(self):
        p = []
        for i in self.genotype:
            if i != 0:
                p.append(i)
        return p

    def get_random_genotype(self):
        return [0 for _ in xrange(self.number_of_gens)]

    def calculate_fitness(self):
        match = 0
        for dist in xrange(len(self.phenotype) - 1 if self.global_sequence else 1):
            for i in xrange(len(self.phenotype) - dist - 1):
                t1 = (self.phenotype[i], self.phenotype[i + 1 + dist])
                for j in xrange(i + 1, len(self.phenotype) - 1 - dist):
                    t2 = self.phenotype[j], self.phenotype[j + 1 + dist]
                    if t2 == t1:
                        match += 1

        self.match = match
        return len(self.phenotype) / (1.0 + match)

    #Create char sequecne of the phenotype
    def phenotype_str(self):
        return " " + "".join(
            [chr(96+ i).capitalize() for i in self.phenotype]) + " Len:" + str(
            len(self.phenotype)) + " Collisions:" + str(self.match)


if __name__ == "__main__":

    best = None
    s = SurprisingSequence(5)
    s.crossover_rate = 0.05
    s.child_pool_size = 200
    s.adult_pool_size = 200
    s.parent_pool_size = 100
    s.set_parent_strategy(Strategies.tournament)
    s.adult_selection_mode = Strategies.GENERATION_MIXING
    Individual.mutation_rate = 0.03
    s.run(True)
    print s.best_individual.phenotype_str(), len(s.best_individual.phenotype), s.best_individual.fitness


