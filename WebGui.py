import web
import FlatLand
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
        flatlands = [FlatLand.FlatLand() for _ in xrange(5)]
        maps = [x.map.tolist() for x in flatlands]
        print(flatlands[0].smell())

        b = "test"
        return render.flatland(maps, [flatlands[0].agent_pos[0], flatlands[0].agent_pos[1]])


class beeragent_web:
    def GET(self):
        i = web.input()
        return render.beeragent()

if __name__ == "__main__":
    app.run()