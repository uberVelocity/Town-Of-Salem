from .agent import Villager, Role, Faction, State

class Lookout(Villager):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, Role.LOOKOUT, Faction.VILLAGER)

    # Print the current visited_by list of the agent (not useful at all and potentially incomplete list)
    def interact(self, other_agent):
        print("I, the Lookout, see that ", other_agent.name, " is being visited by: ", other_agent.visited_by)  # TODO: Resolve this in resolve_night()
        other_agent.visited_by.append(self)  # Append yourself as the person who visited the other agent