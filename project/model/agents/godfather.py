from .agent import Mobster, Role, Faction, Health

class Godfather(Mobster):

    def __init__(self, unique_id, model, interactions=False):
        super().__init__(unique_id, model, Role.GODFATHER, interactions, Faction.MOBSTER, )
        self.order = None
        self.protected = True
    
    def interact(self, other_agent):
        if self.interactions:
            print("I, the Godfather[", self.unique_id, "], am ordering to kill agent ", other_agent.name)
        self.order = other_agent
        other_agent.mafia_voted = True
        
        # If Mafioso is dead, Godfather visits the target himself
        if self.agents[7].health == Health.DEAD:
            other_agent.visited_by.append(self)

    def step(self):
        if self.is_alive():
            self.interact(self.pick_random_villager())
        pass
