from .agent import Mobster, Role, Faction

class Godfather(Mobster):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, Role.GODFATHER, Faction.MOBSTER)
        self.order = None
        self.protected = True
    
    def interact(self, other_agent):
        print("I, the Godfather[", self.unique_id, "], am ordering to kill agent ", other_agent.name)
        self.order = other_agent

    def step(self):
        if self.is_alive():
            self.interact(self.pick_random_villager())
        pass
