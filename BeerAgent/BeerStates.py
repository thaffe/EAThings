class BeerObject:
    globalID = 0

    def __init__(self, pos, type):
        self.pos = pos
        self.type = type
        self.id = BeerObject.globalID
        BeerObject.globalID += 1


class BeerStateManager:

    def __init__(self):
        self.



b1 = BeerObject([1,2],1)
b2= BeerObject([1,2],1)

