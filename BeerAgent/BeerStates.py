class BeerStates:
    def __init__(self):
        self.states = []
        self.object_poses = []
        self.catcher_poses = []

    def save_pos(self, object_pos, agent_pos):
        self.object_poses.append(object_pos)
        self.catcher_poses.append(agent_pos)

    def save_state(self, object_size, res):
        self.states.append({
            'size': object_size,
            'res': res,
            'o': self.object_poses[:],
            'c': self.catcher_poses[:]
        })

        self.object_poses = []
        self.catcher_poses = []

