class BeerStates:
    def __init__(self):
        self.states = []
        self.object_pos = []
        self.catcher_pos = []

    def save_pos(self, object_pos, agent_pos):
        self.object_pos.append(object_pos)
        self.catcher_pos.append(agent_pos)

    def save_state(self, object_size):
        self.states.append({
            'size': object_size,
            'o': self.object_pos,
            'c': self.catcher_pos
        })

        self.object_pos = []
        self.catcher_pos = []

