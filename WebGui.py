import web

from Flatland import Flatland

urls = (
    '/', 'index',
    '/flatland', 'flatland_web',
    '/beeragent', 'beeragent_web'
)
app = web.application(urls, globals())
render = web.template.render('templates/',base='layout')


class index:
    def GET(self):
        return render.index()


class flatland_web:
    def GET(self):
        i = web.input()
        flatlands = [Flatland.Flatland() for _ in xrange(5)]
        maps = [x.map.tolist() for x in flatlands]
        print(flatlands[0].smell())
        return render.flatland(maps, [flatlands[0].agent_pos[0], flatlands[0].agent_pos[1]],{'t':'test'})


class beeragent_web:
    def GET(self):
        i = web.input()

        return render.beeragent([])

if __name__ == "__main__":
    app.run()

