from .agent import Villager, Role, Faction, State

class Sheriff(Villager):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, Role.SHERIFF, Faction.VILLAGER)

    # Print the role of the inspected agent. The Godfather appears as a villager.
    def interact(self, other_agent):
        if other_agent.role == Role.GODFATHER:
            print("I, the Sheriff[", self.unique_id, "], am Inspecting agent ", other_agent.name, " and their faction is ", Faction.VILLAGER)
            other_agent.visited_by.append(self)
        else:
            print("I, the Sheriff[", self.unique_id, "], am Inspecting agent ", other_agent.name, " and their faction is ", other_agent.faction)
            other_agent.visited_by.append(self)