from .agent import Villager, Role, Faction

class Lookout(Villager):

    def __init__(self, unique_id, model, interactions=False):
        super().__init__(unique_id, model, Role.LOOKOUT, interactions, Faction.VILLAGER, )

    # Print the current visited_by list of the agent (not useful at all and potentially incomplete list)
    def interact(self, other_agent):
        other_agent.visited_by.append(self)  # Append yourself as the person who visited the other agent
        self.visiting = other_agent