import web
from beer.BeerEA import BeerEA

from flatland.FlatlandEA import *
from core.Individual import Individual


parentStrat = [
    ('Fitness Proportionate', Strategies.fitness),
    ('Sigma Scaling', Strategies.sigma),
    ('Boltzmann Selection', Strategies.boltz),
    ('Rank Selection', Strategies.rank),
    ('Tournament Selection', Strategies.tournament),
    ('Uniform Selection', Strategies.uniform),
]

adultStrat = [
    "Generation Replacement",
    "Generation Mixing"
]

defaults = {
    'generations': 100,
    'adultStrategy': 0,
    'parentStrategy': 0, #Rank sel, see array over
    'childPool': 50,
    'adultPool': 25,
    'parentPool': 10,
    'mutation': [0.1, 0.1, 0.0, 1.0],
    'crossover': [0.1, 0.1, 0.0, 1.0],
    'rank': [0.5, 1.5],
    'tournament': [5, 0.1],
    'flatland': 0
}

urls = (
    '/', 'index',
    '/settings', 'settings',
    '/flatland', 'flatland_web',
    '/beeragent', 'beeragent_web'
)
app = web.application(urls, globals())
render = web.template.render('templates/', base='layout')
web.template.Template.globals['render'] =  web.template.render('templates/')
web.template.Template.globals['str'] = str

web.template.Template.globals['adultStrat'] = adultStrat
web.template.Template.globals['parentStrat'] = parentStrat


def setup_ea(input):
    EA.max_generations = int(input.generations)
    EA.adult_pool_size = int(input.adultPool)
    EA.child_pool_size = int(input.childPool)
    EA.parent_pool_size = int(input.parentPool)
    EA.adult_selection_mode = int(input.adultStrategy)
    EA.parent_selection_strategy = parentStrat[int(input.parentStrategy)]
    EA.crossover_rate = NormDist(float(input.crossover[0]), float(input.crossover[1]),
                                 float(input.crossover[2]), float(input.crossover[3]))

    Individual.mutation_rate = NormDist(float(input.mutation[0]), float(input.mutation[1]),
                                        float(input.mutation[2]), float(input.mutation[3]))

    Strategies.rank_min = float(input.rank[0])
    Strategies.rank_max = float(input.rank[1])
    Strategies.tournament_k = int(input.tournament[0])
    Strategies.tournament_e = float(input.tournament[1])

    return "T"

class index:
    def GET(self):
        return render.index()


class settings:
    def GET(self):
        i = web.input()
        defaults['game'] = i.game
        return render.settings(defaults, False)


class flatland_web:

    def GET(self):
        i = web.input(tournament=[], rank=[], mutation=[], crossover=[])
        setup_ea(i)
        FlatlandEA.dynamic = i.has_key('flatland')
        i.setdefault('flatland',False)
        ea = FlatlandEA()
        ea.run()
        return render.flatland(ea, i)


class beeragent_web:

    def GET(self):
        i = web.input(tournament=[], rank=[], mutation=[], crossover=[])
        setup_ea(i)
        ea = BeerEA()
        ea.run()
        return render.beeragent(ea,i)


if __name__ == "__main__":
    app.run()

