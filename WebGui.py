import web

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
    def GET(self):
        i = web.input()


        ea = FlatlandEA()
        ea.run()

        print ea.best_individual
        return render.flatland(ea.best_individual.maps)


class beeragent_web:
    def GET(self):
        i = web.input()

        return render.beeragent([])

if __name__ == "__main__":
    app.run()

