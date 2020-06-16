from .agent import Villager, Role, Faction, Health, ActionStrategy
from random import choice

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
        strategy = ActionStrategy.KNOWLEDGE
        if self.is_alive():
            # Picks random agent from alive agents, including self
            if strategy == ActionStrategy.RANDOM:
                self.interact(self.pick_random_agent(False))
            # Picks random agent from known villagers, including self
            elif strategy == ActionStrategy.KNOWLEDGE:
                villagers = []
                
                # Get all villagers from knowledge base
                for id, faction in self.knowledge:
                    if faction == str(Faction.VILLAGER.value) and self.agents[id].health == Health.ALIVE:
                        villagers.append(id)
                if self.interactions:
                    print("List of potential guarding buddies: ", villagers)

                # Guard random agent if Bodyguard knows only about themself
                if len(villagers) == 1:
                    self.interact(self.pick_random_agent(False))
                else:
                    # Always guard town member if Bodyguard cannot guard self
                    if self.vests == 0:
                        villagers.remove(self.name)
                    self.interact(self.agents[choice(villagers)])