from .agent import Villager, Role, Faction

class Doctor(Villager):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, Role.DOCTOR, Faction.VILLAGER)
        self.self_heals = 1

    # Pick any agent from the game, including self and give them PROTECTED
    def interact(self, other_agent):
        if other_agent != self:
            print("I, the Doctor[", self.unique_id, "], am Healing ", other_agent.name)
            other_agent.protected = True  # Give other_agent invulnerability for the night
            other_agent.visited_by.append(self)  # Append doctor to other agent's visited by list
            self.visiting = other_agent
        else:
            if self.self_heals != 0:
                print("I, the Doctor[", self.unique_id,"], am Healing myself")
                self.protected = True  # Give invulnerability to self
                self.visiting = self
                self.self_heals = 0

    # Custom step of Doctor: is able to pick themselves
    def step(self):
        if self.is_alive():
            self.interact(self.pick_random_agent(False))
        pass