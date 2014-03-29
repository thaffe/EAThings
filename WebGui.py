import web
from beer.BeerEA import BeerEA

from flatland.FlatlandEA import *

urls = (
    '/', 'index',
    '/flatland', 'flatland_web',
    '/beer', 'beeragent_web'
)
app = web.application(urls, globals())
render = web.template.render('templates/',base='layout')


class index:
    def GET(self):
        return render.index()


class flatland_web:

    def __init__(self):
        self.ea = FlatlandEA()

    def GET(self):
        i = web.input()

        self.ea.child_pool_size = 10
        self.ea.parent_pool_size = 10
        self.ea.adult_pool_size = 5
        self.ea.run()

        print self.ea.maps[0].agent_pos, self.ea.maps[0].agent_direction.val
        return render.flatland(self.ea.maps)


class beeragent_web:

    def __init__(self):
        self.ea = BeerEA()

    def GET(self):
        i = web.input()

        return render.beeragent([])

if __name__ == "__main__":
    app.run()

