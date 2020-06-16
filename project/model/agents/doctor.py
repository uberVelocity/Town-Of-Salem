from .agent import Villager, Role, Faction, Health, ActionStrategy
from random import choice
class Doctor(Villager):

    def __init__(self, unique_id, model, interactions=False):
        super().__init__(unique_id, model, Role.DOCTOR, interactions, Faction.VILLAGER)
        self.self_heals = 1

    # Pick any agent from the game, including self and give them PROTECTED
    def interact(self, other_agent):
        if other_agent != self:
            if self.interactions:
                print("I, the Doctor[", self.unique_id, "], am Healing ", other_agent.name)
            other_agent.protected = True  # Give other_agent invulnerability for the night
            other_agent.visited_by.append(self)  # Append doctor to other agent's visited by list
            self.visiting = other_agent
        else:
            if self.self_heals != 0:
                if self.interactions:
                    print("I, the Doctor[", self.unique_id,"], am Healing myself")
                self.protected = True  # Give invulnerability to self
                self.visiting = self
                self.self_heals = 0

    # Custom step of Doctor: is able to pick themselves
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
                print("List of potential healing buddies: ", villagers)

                # Heal random agent if Doctor knows only about themself
                if len(villagers) == 1:
                    self.interact(self.pick_random_agent(False))
                else:
                    # Always heal town member if Doctor cannot heal self
                    if self.self_heals == 0:
                        villagers.remove(self.name)
                    self.interact(self.agents[choice(villagers)])
        pass