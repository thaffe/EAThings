import json
from threading import Thread

import web

from beer.BeerEA import BeerEA
from flatland.FlatlandEA import *


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
    'adultStrategy': 1,
    'parentStrategy': 3, #Rank sel, see array over
    'childPool': 100,
    'adultPool': 50,
    'parentPool': 30,
    'mutation': [-0.2, 0.3, 0.0, 1.0],
    'crossover': [0.3, 0.2, 0.0, 1.0],
    'rank': [0.5, 1.5],
    'tournament': [5, 0.1],
    'flatland': 0
}

urls = (
    '/', 'index',
    '/settings', 'settings',
    '/flatland', 'flatland_web',
    '/beeragent', 'beeragent_web',
    '/start', 'starter',
    '/progress', 'progress'
)
app = web.application(urls, globals())
render = web.template.render('templates/', base='layout')
web.template.Template.globals['render'] = web.template.render('templates/')
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

    EA.mutation_rate = NormDist(float(input.mutation[0]), float(input.mutation[1]),
                                float(input.mutation[2]), float(input.mutation[3]))

    Strategies.rank_min = float(input.rank[0])
    Strategies.rank_max = float(input.rank[1])
    Strategies.tournament_k = int(input.tournament[0])
    Strategies.tournament_e = float(input.tournament[1])

    return "T"


current_ea = None
ea_thread = None
current_game = None


def start_ea(ea):
    print("startingEA")
    ea.run()


class index:
    def GET(self):
        return render.index()


class settings:
    def GET(self):
        i = web.input()
        defaults['game'] = i.game
        return render.settings(defaults, False)


class starter:
    def GET(self):
        global ea_thread, current_ea, current_game
        i = web.input(tournament=[], rank=[], mutation=[], crossover=[])
        setup_ea(i)
        current_game = i.game
        current_ea = FlatlandEA() if i.game == "flatland" else BeerEA()
        ea_thread = Thread(target=start_ea, args=[current_ea])
        ea_thread.start()
        web.header('Content-Type', 'application/json')
        return json.dumps({'start': True})


class progress:
    def GET(self):
        global ea_thread, current_ea, current_game
        web.header('Content-Type', 'application/json')
        complete = current_ea.current_generation == EA.max_generations
        res = {
            'complete': complete
        }
        if complete:
            res['means'] = current_ea.means
            res['sds'] = current_ea.sds
            res['bests'] = current_ea.bests
            res['similarity'] = current_ea.best_similarities
            res['fitness'] = current_ea.best_individual.fitness

            if current_game == 'beeragent':
                res['game'] = current_ea.best_history.states
            else:
                res['game'] ={
                    'maps':[flatland.map.tolist() for flatland in current_ea.best_maps],
                    'botPos':[list(flatland.agent_pos) for flatland in current_ea.best_maps],
                    'hists':[flatland.history for flatland in current_ea.best_maps],
                    'botDir':[flatland.agent_direction.val.tolist() for flatland in current_ea.best_maps],
                    'mapRes':[[flatland.food_gathered,flatland.poisoned] for flatland in current_ea.best_maps]
                }

        else:
            best_fitness = current_ea.best_individual.fitness if current_ea.best_individual else 0
            res = {
                'm': "Generation: %d of %d Best:%2.f" % (current_ea.current_generation, EA.max_generations, best_fitness)}

        return json.dumps(res)


class flatland_web:
    def GET(self):
        defaults['game'] = "flatland"
        return render.flatland(defaults)


class beeragent_web:
    def GET(self):
        defaults['game'] = "beeragent"
        return render.beeragent(defaults)


if __name__ == "__main__":
    app.run()

