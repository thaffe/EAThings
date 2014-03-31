from ann.ANN import ANN
from core.AnnIndividual import AnnIndividual
from core.GeneFloat import GeneFloatSource
from flatland.Flatland import Flatland


class FlatlandAgent(AnnIndividual):
    source = [
        {"name": "ff", "pre_update": None, "data": None},
        {"name": "fl", "pre_update": None, "data": None},
        {"name": "fr", "pre_update": None, "data": None},
        {"name": "pf", "pre_update": None, "data": None},
        {"name": "pl", "pre_update": None, "data": None},
        {"name": "pr", "pre_update": None, "data": None},
        {"name": "f", "weights": {"ff": 0, "pf": 0}, "post_update": None, "data": None},
        {"name": "l", "weights": {"fl": 0, "pl": 0}, "post_update": None, "data": None},
        {"name": "r", "weights": {"fr": 0, "pr": 0}, "post_update": None, "data": None}
    ]

    tau_source = GeneFloatSource(1, 1, False)
    g_source = GeneFloatSource(1, 1, False)
    bias_source = GeneFloatSource(0.0, 0.0, False)
    weight_source = GeneFloatSource(-1.0, 1.0, False)

    def __init__(self, mutation_rate, genotype=None):
        AnnIndividual.__init__(self, mutation_rate, genotype)
        self.flat_land = Flatland()

    def phenotype_str(self):
        return "IM a flatland dude"

    def get_move_from_smell(self, smell, step):
        # print [[input.weight for _, input in neuron.inputs.items()] for _, neuron in self.ann.neurons.items()]
        for node in ["ff", "fl", "fr", "pf", "pr", "pl"]:
            self.ann.neurons[node].output = 0.0
            self.ann.neurons[node].step_counter = step

        if smell[0] and smell[0] != '0':
            self.ann.neurons[smell[0] + "f"].output = 1.0
        if smell[1] and smell[1] != '0':
            self.ann.neurons[smell[1] + "l"].output = 1.0
        if smell[2] and smell[2] != '0':
            self.ann.neurons[smell[2] + "r"].output = 1.0

        move = "n"
        best = -0.5

        if self.ann.neurons["f"].update(step) > best:
            move = "f"
            best = self.ann.neurons["f"].update(step)
        if self.ann.neurons["l"].update(step) > best:
            move = "l"
            best = self.ann.neurons["l"].update(step)
        if self.ann.neurons["r"].update(step) > best:
            move = "r"

        return move
