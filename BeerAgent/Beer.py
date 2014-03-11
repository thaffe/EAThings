

class Beer:

    Width = 30
    Height = 15

    def __init__(self, agent_pos=0, object_pos=0):
        self.agent_pos = 0
        self.object_pos = 0
        self.object_size = 3
        self.steps_left = self.Height

    def timestep(self):
        self.agent_pos += agent.getmove()
        self.object_pos +=