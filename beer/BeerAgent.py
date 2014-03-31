from ann.ANN import ANN
from core.AnnIndividual import AnnIndividual


class BeerAgent(AnnIndividual):

    source = [
        {"name": "s0", "pre_update": None, "data": None},
        {"name": "s1", "pre_update": None, "data": None},
        {"name": "s2", "pre_update": None, "data": None},
        {"name": "s3", "pre_update": None, "data": None},
        {"name": "s4", "pre_update": None, "data": None},
        {"name": "h0", "weights": {"s0": 0, "s1": 0, "s2": 0, "s3": 0, "s4": 0}, "post_update": None, "data": None},
        {"name": "h1", "weights": {"s0": 0, "s1": 0, "s2": 0, "s3": 0, "s4": 0}, "post_update": None, "data": None},
        {"name": "o0", "weights": {"h0": 0, "h1": 0}, "post_update": None, "data": None},
        {"name": "o1", "weights": {"h0": 0, "h1": 0}, "post_update": None, "data": None}
    ]

    def calculate_fitness(self):
        pass

    def phenotype_str(self):
        return "I'm a BeerAgent!"

    def getmove(self, shadows, step):
        for i in xrange(5):
            self.ann.neurons["s" + str(i)].output = shadows[i]

        return - self.ann.neurons["o0"].update(step) if self.ann.neurons["o0"].output > self.ann.neurons["o1"].output \
            else self.ann.neurons["o1"].update(step)
