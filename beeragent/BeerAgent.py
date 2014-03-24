from ann.ANN import ANN
from core.Individual import Individual


class BeerAgent(Individual):

    source = ANN(neurons=[
        {"name": "s0", "pre_update": None, "data": None},
        {"name": "s1", "pre_update": None, "data": None},
        {"name": "s2", "pre_update": None, "data": None},
        {"name": "s3", "pre_update": None, "data": None},
        {"name": "s4", "pre_update": None, "data": None},
        {"name": "h0", "weights": {"s0": 0, "s1": 0, "s2": 0, "s3": 0, "s4": 0}, "post_update": None, "data": None},
        {"name": "h1", "weights": {"s0": 0, "s1": 0, "s2": 0, "s3": 0, "s4": 0}, "post_update": None, "data": None},
        {"name": "o0", "weights": {"h0": 0, "h1": 0}, "post_update": None, "data": None},
        {"name": "o1", "weights": {"h0": 0, "h1": 0}, "post_update": None, "data": None}
    ])

    def calculate_fitness(self):
        pass

    def generate_phenotype(self):
        pass

    def random_genotype(self):
        pass

    def phenotype_str(self):
        return "I'm a BeerAgent!"