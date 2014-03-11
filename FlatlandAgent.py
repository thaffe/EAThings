from ANN import ANN
from EA import *
from FlatLand import FlatLand


class FlatlandAgent(EA):

    def create_individual(self, genotype=None):
        return FlatlandIndividual(genotype)


class FlatlandIndividual(ANN_Individual):

    def __init__(self, genotype):
        ANN.__init__(self, genotype)
        self.flat_land = FlatLand()

    def generate_phenotype(self):

        return self.genotype

    def calculate_fitness(self):
        return 0

    def phenotype_str(self):
        return "IM a flatland dude"