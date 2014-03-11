from abc import abstractmethod
import math
from EA import Individual


class ANN_Individual(Individual):

    ann = None

    def __init__(self, genotype=None):
        if not genotype:
            genotype = []
            for neuron in self.ann.neurons:
                genotype.append(0)
                for _ in neuron.inputs:
                    genotype.append(0)
            self.phenotype = self.ann

        Individual.__init__(self, genotype)

    def generate_phenotype(self):
        index = 0
        for neuron in self.ann.neurons:
            neuron.memory = self.genotype[index]
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
    def __init__(self):
        self.neurons = {}

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