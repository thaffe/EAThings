from EA import *
import cProfile

class OneMax(EA):
    def __init__(self, bits=20, random=False):
        EA.__init__(self, bits)
        print("INTI ONE MAX",bits)
        Individual.number_of_gens = bits
        Individual.number_of_gene_symbols = 2
        if random: OneMaxIndividual.goal = [randint(0, 1) for _ in xrange(bits)]

    def create_individual(self, genotype=None):
        return OneMaxIndividual(genotype)


class OneMaxIndividual(Individual):
    goal = None

    def generate_phenotype(self):
        return self.genotype

    def calculate_fitness(self):
        #
        if self.goal is None:
            return sum(self.phenotype)
        return sum(self.phenotype[i] == self.goal[i] for i in xrange(self.number_of_gens))

    def phenotype_str(self):
        return "".join(["1" if i else "0" for i in self.phenotype])


if __name__ == "__main__":
    e = OneMax(40)
    #Set strategy

    e.run(True)