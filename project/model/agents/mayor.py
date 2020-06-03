from random import randint

from .agent import Villager, Role, Faction, State

class Mayor(Villager):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, Role.MAYOR, Faction.VILLAGER)
        self.revealed = False

    # Reveal yourself as the mayor to the townspeople.
    def interact(self, other_agent):
        if randint(0, 9) < 3 and not self.revealed:
            print("I, the Mayor[", self.unique_id, "], have revealed myself")
            self.revealed = True
        else:
            print("I, the Mayor[", self.unique_id, "], am doing nothing")