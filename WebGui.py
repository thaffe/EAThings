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
        ea.child_pool_size = 10
        ea.parent_pool_size = 10
        ea.adult_pool_size = 5
        ea.run()

        print ea.maps[0].agent_pos, ea.maps[0].agent_direction.val
        return render.flatland(ea.maps)


class beeragent_web:
    def GET(self):
        i = web.input()

        return render.beeragent([])

if __name__ == "__main__":
    app.run()

