from abc import abstractmethod
from copy import deepcopy
import math
from Individual import Individual
from GeneFloat import GeneFloat, GeneFloatSource


class AnnIndividual(Individual):

    source = None

    tau_source = GeneFloatSource(0.01, 100, True)
    g_source = GeneFloatSource(0.01, 100, True)
    bias_source = GeneFloatSource(-1.0, 1.0, False)
    weight_source = GeneFloatSource(-1, 1, False)

    def random_genotype(self):
        self.genotype = []
        for neuron in self.source.neurons:
            self.genotype.append(GeneFloat(source=self.tau_source))
            self.genotype.append(GeneFloat(source=self.g_source))
            self.genotype.append(GeneFloat(source=self.bias_source))
            for _ in neuron.inputs:
                self.genotype.append(GeneFloat(source=self.weight_source))

    def generate_phenotype(self):
        index = 0
        # TODO: Uvisst om man er nødt til å gjøre mer her, for at ikke pheno (ann) bare blir static.
        self.ann = deepcopy(self.source)
        for key, neuron in self.ann.neurons:
            neuron.tau = self.genotype[index]
            index += 1
            neuron.g = self.genotype[index]
            index += 1
            neuron.bias = self.genotype[index]
            index += 1
            for input in neuron.inputs:
                input.weight = self.genotype[index]
                index += 1

    @abstractmethod
    def calculate_fitness(self):
        pass

    def phenotype_str(self):
        pass


class ANN:
    def __init__(self, neurons=None):
        self.neurons = {}
        if neurons:
            for neuron in neurons:
                self.append(neuron)

    def append(self, name, weights=None, pre_update=None, post_update=None, always_update=False, data=None, tau=1.0, g=1.0, bias=0.0):
        if not weights:
            weights = []
        inputs = {}
        for key in weights:
            inputs[key] = Input(self.neurons[key], weights[key])
        self.neurons[name] = Neuron(name, inputs, pre_update, post_update, always_update, data, tau, g, bias)

    def update(self, step_counter):
        for neuron in self.neurons:
            n = self.neurons[neuron]
            if n.step_counter != step_counter and n.always_update:
                n.update(step_counter)

    def set_weight(self, neuron_name, input_name, weight):
        self.neurons[neuron_name].inputs[input_name].weight = weight


class Neuron:

    def __init__(self, name, inputs, pre_update=None, post_update=None, always_update=False, data=None, tau=1.0, g=1.0, bias=0.0):
        self.name = name
        self.inputs = inputs
        self.pre_update = pre_update
        self.post_update = post_update
        self.always_update = always_update
        self.data = data
        self.step_counter = 0

        self.tau = tau
        self.g = g
        self.bias = bias

        self.si = 0
        self.y = self.bias
        self.output = 0

    def update(self, step_counter):
        if self.pre_update:
            self.pre_update(self)

        si = 0
        for key in self.inputs:
            input = self.inputs[key]
            if input.neuron.step_counter != step_counter:
                input.neuron.update(step_counter)
            si += input.neuron.output * input.weight

        dy = (-self.y + si + self.bias) / self.tau
        self.y += dy
        self.output = 1 / (1 + math.exp(-self.g * self.y))
        self.step_counter = step_counter

        if self.post_update:
            self.post_update(self)
        return self.output


class Input:
    def __init__(self, neuron, weight):
        self.neuron = neuron
        self.weight = weight
        self.activated = True