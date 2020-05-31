from .agent import Villager, Role, Faction, State

class Doctor(Villager):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, Role.DOCTOR, Faction.VILLAGER)
        self.self_heals = 1

    # Pick any agent from the game, including self and give them PROTECTED
    def interact(self, other_agent):
        other_agent.State = State.PROTECTED  # Give agents invulnerability for the night
        if other_agent != self:
            other_agent.visited_by.append(self)  # Append doctor to other agent's visited by list
        else:
            self.self_heals = 0

    # Custom step of Doctor: is able to pick themselves
    def step(self):
        self.interact(self.pick_random_agent(0))
        pass