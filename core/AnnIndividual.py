from abc import abstractmethod
from ann.ANN import ANN
from core.GeneFloat import GeneFloat, GeneFloatSource
from core.Individual import Individual


class AnnIndividual(Individual):

    source = None

    tau_source = GeneFloatSource(0.1, 10, True)
    g_source = GeneFloatSource(0.1, 10, True)
    bias_source = GeneFloatSource(-1, 1, False)
    weight_source = GeneFloatSource(-1.0, 1.0, False)

    def __init__(self, mutation_rate, genotype=None):
        self.ann = ANN(self.source)
        Individual.__init__(self, mutation_rate, genotype)

    def random_genotype(self):
        self.genotype = []
        for key, neuron in self.ann.neurons.items():
            self.genotype.append(GeneFloat(source=self.tau_source))
            self.genotype.append(GeneFloat(source=self.g_source))
            self.genotype.append(GeneFloat(source=self.bias_source))
            for _ in neuron.inputs:
                self.genotype.append(GeneFloat(source=self.weight_source))

    def generate_phenotype(self):
        index = 0
        for key, neuron in self.ann.neurons.items():
            neuron.tau = self.genotype[index].value
            index += 1
            neuron.g = self.genotype[index].value
            index += 1
            neuron.bias = self.genotype[index].value
            index += 1
            for key, input in neuron.inputs.items():
                input.weight = self.genotype[index].value
                index += 1

    @abstractmethod
    def calculate_fitness(self):
        pass

    def phenotype_str(self):
        pass
