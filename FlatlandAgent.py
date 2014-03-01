from EA import *

class FlatlandAgent(EA):

    def create_individual(self, genotype=None):
        return FlatlandIndividual(genotype)


class FlatlandIndividual(Individual):
    def generate_phenotype(self):
        return self.genotype

    def calculate_fitness(self):
        return 0

    def phenotype_str(self):
        return "IM a flatland dude"