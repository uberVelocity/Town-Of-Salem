from .agent import Villager, Role, Faction

class Sheriff(Villager):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, Role.SHERIFF, Faction.VILLAGER)

    # A sheriff visits someone and gets their faction
    def interact(self, other_agent):
        other_agent.visited_by.append(self)
        self.visiting = other_agent
