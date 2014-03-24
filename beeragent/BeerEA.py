from beeragent.BeerAgent import BeerAgent
from core.EA import EA


class BeerEA(EA):

    def create_individual(self, genotype=None):
        return BeerAgent(genotype)