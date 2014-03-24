from abc import abstractmethod
from copy import deepcopy


class Gene():
    size = 1

    def __init__(self, replica=None, source=None):
        self.gene_size = 1
        if replica:
            self.genotype = deepcopy(replica)
            self.mutate()
        else:
            self.random_value(source)

    @abstractmethod
    def mutate(self, mutation_rate):
        pass

    @abstractmethod
    def random_value(self, source):
        pass