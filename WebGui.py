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
        maps = [FlatLand.FlatLand().map.tolist() for _ in xrange(5)]
        b = "test"
        return render.flatland(maps,b)


class beeragent_web:
    def GET(self):
        i = web.input()
        return render.beeragent()

if __name__ == "__main__":
    app.run()