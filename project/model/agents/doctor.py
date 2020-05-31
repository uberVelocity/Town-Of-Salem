from .agent import Villager, Role, Faction, State

class Doctor(Villager):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, Role.DOCTOR, Faction.VILLAGER)
        self.self_heals = 1

    # Pick any agent from the game, including self and give them PROTECTED
    def interact(self, other_agent):
        self.pick_random_agent(1).State = State.PROTECTED