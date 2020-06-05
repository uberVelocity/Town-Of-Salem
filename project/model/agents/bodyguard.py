from .agent import Villager, Role, Faction

class Bodyguard(Villager):

    def __init__(self, unique_id, model, interactions=False):
        super().__init__(unique_id, model, Role.BODYGUARD, interactions, Faction.VILLAGER)
        self.vests = 1

    # Prints who they're bodyguarding.
    def interact(self, other_agent):
        if not other_agent == self:
            other_agent.protected = True
            if self.interactions:
                print("I, the Bodyguard[", self.unique_id, "], am guarding agent ", other_agent.name)
            other_agent.visited_by.append(self)
            self.visiting = other_agent
        else:
            if self.vests == 1:
                self.vests = 0
                self.protected = True
                self.visiting = self
                if self.interactions:
                    print("I, the Bodyguard[", self.unique_id, "], am guarding myself")

    # Custom step of Bodyguard: is able to guard themselves
    def step(self):
        if self.is_alive():
            self.interact(self.pick_random_agent(False))
        pass