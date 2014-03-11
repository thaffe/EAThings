class BeerObject:
    globalID = 0

    def __init__(self, pos, type):
        self.pos = pos
        self.type = type
        self.id = BeerObject.globalID
        BeerObject.globalID += 1


class BeerStateManager:

    def __init__(self):
        self.states =[]


    def store(self, timePased, objects):
        self.states.append("THINGS AND STUFF")

