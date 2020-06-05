from .agent import Villager, Role, Faction

class Bodyguard(Villager):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, Role.BODYGUARD, Faction.VILLAGER)

    # Prints who they're bodyguarding.
    def interact(self, other_agent):
        if not other_agent == self:
            other_agent.protected = True
            print("I, the Bodyguard[", self.unique_id, "], am guarding agent ", other_agent.name)
            other_agent.visited_by.append(self)
            self.visiting = other_agent
        else:
            self.protected = True
            self.visiting = self
            print("I, the Bodyguard[", self.unique_id, "], am guarding myself")
        pass

    # Custom step of Bodyguard: is able to guard themselves
    def step(self):
        if self.is_alive():
            self.interact(self.pick_random_agent(False))
        pass