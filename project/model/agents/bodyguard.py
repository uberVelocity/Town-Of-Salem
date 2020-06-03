from .agent import Villager, Role, Faction, State

class Bodyguard(Villager):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, Role.BODYGUARD, Faction.VILLAGER)

    # Prints who they're bodyguarding.
    def interact(self, other_agent):
        if not other_agent == self:
            other_agent.state = State.PROTECTED
            print("I, the Bodyguard[", self.unique_id, "], am guarding agent ", other_agent.name)
            other_agent.visited_by.append(self)
        else:
            self.state = State.PROTECTED
            print("I, the Bodyguard[", self.unique_id, "], am guarding myself")
        pass

    # Custom step of Bodyguard: is able to guard themselves
    def step(self):
        self.interact(self.pick_random_agent(0))
        pass