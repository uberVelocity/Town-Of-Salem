from .agent import Villager, Role, Health, Faction, ActionStrategy
from random import choice

class Lookout(Villager):

    def __init__(self, unique_id, model, interactions=False):
        super().__init__(unique_id, model, Role.LOOKOUT, interactions, Faction.VILLAGER)

    # Print the current visited_by list of the agent (not useful at all and potentially incomplete list)
    def interact(self, other_agent):
        other_agent.visited_by.append(self)  # Append yourself as the person who visited the other agent
        self.visiting = other_agent

    def step(self):
        strategy = ActionStrategy.KNOWLEDGE
        if self.is_alive():
            if strategy == ActionStrategy.RANDOM:
                self.interact(self.pick_random_agent(True))
            elif strategy == ActionStrategy.KNOWLEDGE:
                villagers = []

                # Get all villagers from knowledge base
                for id, faction in self.knowledge:
                    if faction == str(Faction.VILLAGER.value) and self.agents[id].health == Health.ALIVE:
                        villagers.append(id)

                if len(villagers) == 1:
                    self.interact(self.pick_random_agent(False))
                else:
                    villagers.remove(self.name)
                    self.interact(self.agents[choice(villagers)])