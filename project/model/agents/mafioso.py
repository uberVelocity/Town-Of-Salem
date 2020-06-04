from .agent import Mobster, Role, Faction

class Mafioso(Mobster):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, Role.MAFIOSO, Faction.MOBSTER)

    # Targets another agent to kill
    def interact(self, other_agent):
        if other_agent.is_alive():
            other_agent.attacked = True
            print("I, the Mafioso[", self.unique_id, "], am Voting to Kill agent ", other_agent.name)
            other_agent.visited_by.append(self)
            self.visiting = other_agent
    
    def step(self):
        if self.is_alive():
            self.interact(self.pick_random_villager())
        pass
