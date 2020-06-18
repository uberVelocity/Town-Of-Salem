from .agent import Villager, Role, Faction, Health, ActionStrategy
from random import choice
from copy import copy

class Sheriff(Villager):

    def __init__(self, unique_id, model, interactions=False):
        super().__init__(unique_id, model, Role.SHERIFF, interactions, Faction.VILLAGER)

    # A sheriff visits someone and gets their faction
    def interact(self, other_agent):
        other_agent.visited_by.append(self)
        self.visiting = other_agent

    def step(self):
        strategy = ActionStrategy.KNOWLEDGE
        if self.is_alive():
            # Picks random agent from alive agents, including self
            if strategy == ActionStrategy.RANDOM:
                self.interact(self.pick_random_agent(False))
            # Picks random agent from known villagers, including self
            elif strategy == ActionStrategy.KNOWLEDGE:
                unknown = copy(self.agents)
                
                # Get all villagers from knowledge base
                for id, faction in self.knowledge:
                    unknown.remove(self.agents[id])
                if self.interactions:
                    print("List of potential target buddies: ", unknown)
                if len(unknown) != 0:
                    self.interact(self.agents[choice(unknown).name])