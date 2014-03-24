from ann.ANN import ANN
from core.AnnIndividual import AnnIndividual
from flatland.Flatland import Flatland


class FlatlandAgent(AnnIndividual):

    source = ANN(neurons=[
        {"name": "ff", "pre_update": None, "data": None},
        {"name": "fl", "pre_update": None, "data": None},
        {"name": "fr", "pre_update": None, "data": None},
        {"name": "pf", "pre_update": None, "data": None},
        {"name": "pl", "pre_update": None, "data": None},
        {"name": "pr", "pre_update": None, "data": None},
        {"name": "f", "weights": {"ff": 0, "pf": 0}, "post_update": None, "data": None},
        {"name": "l", "weights": {"fl": 0, "pl": 0}, "post_update": None, "data": None},
        {"name": "r", "weights": {"fr": 0, "pr": 0}, "post_update": None, "data": None}
    ])

    def __init__(self, genotype):
        AnnIndividual.__init__(self, genotype)
        self.flat_land = Flatland()

    def calculate_fitness(self):
        return 0

    def phenotype_str(self):
        return "IM a flatland dude"

    def get_move_priorities(self, smell, step):
        self.ann.neurons["ff"].output = 0.0
        self.ann.neurons["ff"].stepcounter = step
        self.ann.neurons["fl"].output = 0.0
        self.ann.neurons["fl"].stepcounter = step
        self.ann.neurons["fr"].output = 0.0
        self.ann.neurons["fr"].stepcounter = step
        self.ann.neurons["pf"].output = 0.0
        self.ann.neurons["pf"].stepcounter = step
        self.ann.neurons["pl"].output = 0.0
        self.ann.neurons["pl"].stepcounter = step
        self.ann.neurons["pr"].output = 0.0
        self.ann.neurons["pr"].stepcounter = step

        if smell[0]:
            self.ann.neurons["f" + smell[0]].output = 1.0
        if smell[1]:
            self.ann.neurons["f" + smell[1]].output = 1.0
        if smell[2]:
            self.ann.neurons["f" + smell[2]].output = 1.0

        move_strengths = [self.ann.neurons["f"].update(step), self.ann.neurons["l"].update(step),
                          self.ann.neurons["r"].update(step)]
        moves = []
        best = 0
        if move_strengths[0] > 0.5:
            moves.append('f')
        if move_strengths[1] > 0.5:
            if move_strengths[1] > move_strengths[0]:
                moves.insert(0, 'l')
                best = 1
            else:
                moves.append('l')
        if move_strengths[2] > 0.5:
            if move_strengths[2] > move_strengths[best]:
                moves.insert(0, 'r')
            elif move_strengths[2] > move_strengths[1 - best]:
                moves.insert(1, 'r')
            else:
                moves.append('r')
        moves.append('n')

        return moves
