from .agent import Mobster, Role, Faction, State

class Godfather(Mobster):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, Role.GODFATHER, Faction.MOBSTER)
    
    def interact(self, other_agent):
        print("I, the Godfather[", self.unique_id, "], am ordering to kill agent ", other_agent.name)

    def step(self):
        self.interact(self.pick_random_villager())
        pass
