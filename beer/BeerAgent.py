from core.AnnIndividual import AnnIndividual
from core.GeneFloat import GeneFloatSource


class BeerAgent(AnnIndividual):

    source = [
        {"name": "s0"},
        {"name": "s1"},
        {"name": "s2"},
        {"name": "s3"},
        {"name": "s4"},
        {"name": "h0", "weights": {"s0": 0, "s1": 0, "s2": 0, "s3": 0, "s4": 0}},
        {"name": "h1", "weights": {"s0": 0, "s1": 0, "s2": 0, "s3": 0, "s4": 0, "h0": 0}},
        # {"name": "h2", "weights": {"s0": 0, "s1": 0, "s2": 0, "s3": 0, "s4": 0, "h0": 0, "h1": 0}},
        {"name": "o0", "weights": {"h0": 0, "h1": 0}}, #, "h2": 0}},
        {"name": "o1", "weights": {"h0": 0, "h1": 0, "o0": 0}} #"h1": 0, "h2": 0, "o0": 0}}
    ]

    source_appends = [
        # {"name": "h0", "weights": {"h1": 0}}, #"h2": 0}},
        # {"name": "h1", "weights": {"h2": 0}},
        {"name": "o0", "weights": {"o1": 0}}
    ]

    tau_source = GeneFloatSource(1, 2, True)
    g_source = GeneFloatSource(1, 5, False)
    bias_source = GeneFloatSource(-10, 10, False)
    weight_source = GeneFloatSource(-5, 5, False)


    def calculate_fitness(self):
        pass

    def phenotype_str(self):
        return "I'm a BeerAgent!"

    def getmove(self, shadows, step):
        for i in xrange(5):
            n = self.ann.neurons["s" + str(i)]
            n.output = shadows[i]
            n.step_counter = step

        right = self.ann.neurons["o0"].update(step)
        left = self.ann.neurons["o1"].update(step)
        return max(-4, min(4, (left-right)*10))
