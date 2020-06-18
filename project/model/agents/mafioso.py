from .agent import Mobster, Role, Faction

class Mafioso(Mobster):

    def __init__(self, unique_id, model, interactions=False):
        super().__init__(unique_id, model, Role.MAFIOSO, interactions, Faction.MOBSTER)

    # Targets another agent to kill
    def interact(self, other_agent):
        if other_agent.is_alive():
            other_agent.attacked = True
            if self.interactions:
                print("I, the Mafioso[", self.unique_id, "], am Attempting to Kill agent ", other_agent.name)
            other_agent.visited_by.append(self)
            self.visiting = other_agent
    
    def step(self):
        target = None
        if self.is_alive():
            for agent in self.agents:
                if agent.mafia_voted:
                    target = agent
                    break
            if target is not None:
                self.interact(target)
            else:
                self.interact(self.pick_random_villager())
        pass
