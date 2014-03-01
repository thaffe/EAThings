import web

from OneMax import *
from SurprisingSequence import *


urls = (
    '/(.*)', 'index'
)
app = web.application(urls, globals())
render = web.template.render('templates/')

ps = [
    ('Fittness Proportionate', Strategies.fitness),
    ('Sigma Scaling', Strategies.sigma),
    ('Boltzmann Selection', Strategies.boltz),
    ('Rank Selection', Strategies.rank),
    ('Tournament Selection', Strategies.tournament),
    ('Uniform Selection', Strategies.uniform),
]

adultstrat = [
    "Generation Replacement",
    "Generation Mixing"
]

puzzle = [
    ("OneMax", OneMax),
    ("Surprising Sequence", SurprisingSequence)
]


class index:
    def GET(self, name):
        i = web.input()
        if not i.has_key("puzzle"):
            return render.index(ps, adultstrat, puzzle)

        puzzle_index = int(i.puzzle) - 1
        parent_strategy = int(i.parentStrategy) - 1

        if puzzle_index == 0:
            args = [int(i.bits), i.has_key("randomTarget") and bool(i.randomTarget)]
        else:
            args = [int(i.seqSymbols),not i.has_key("seqLocal") ]

        ea = puzzle[puzzle_index][1](*args)
        ea.adult_selection_mode = int(i.adultStrategy) - 1
        ea.adult_pool_size = int(i.adultPool)
        ea.child_pool_size = int(i.childPool)
        ea.parent_pool_size = int(i.parentPool)
        ea.max_generations = int(i.maxgen)
        ea.set_parent_strategy(ps[parent_strategy][1])
        ea.crossover_rate = float(i.crossover) / 100.0

        Individual.mutation_rate = float(i.mutation) / 100.0

        other = []
        if parent_strategy == 3:
            Strategies.rank_min = float(i.rankMin)
            Strategies.rank_max = float(i.rankMax)
            other.append(("Rank Min:", i.rankMin))
            other.append(("RankMax:", i.rankMax))
        elif parent_strategy == 4:
            Strategies.tournament_k = int(i.tourK)
            Strategies.tournament_e = int(i.tourE) / 100.0
            other.append(("Tournament K:", i.tourK))
            other.append(("Tournament E:", i.tourE + "%"))

        ea.run()
        print(ea.fitness_goal)
        return render.running(ea, [
                                      ('Puzzle', puzzle[puzzle_index][0]),
                                      ('Best fittness', ea.best_individual.fitness),
                                      ('Fitness Goal', ea.fitness_goal),
                                      ('Rached Generation', ea.current_generation),
                                      ('Adult Strategy', adultstrat[ea.adult_selection_mode] + (
                                          " with Overproduction" if ea.adult_pool_size < ea.child_pool_size else "")),
                                      ('Parent Strategy', ps[parent_strategy][0]),
                                      ('Child Pool Size', ea.child_pool_size),
                                      ('Adult Pool Size', ea.adult_pool_size),
                                      ('Parent Pool Size', ea.parent_pool_size),
                                      ('Mutation rate', i.mutation + "%"),
                                      ('Crossover rate', i.crossover + "%"),
                                  ] + other)


if __name__ == "__main__":
    app.run()