from random import randint

from .agent import Villager, Role, Faction

class Mayor(Villager):

    def __init__(self, unique_id, model, interactions=False):
        super().__init__(unique_id, model, Role.MAYOR, interactions, Faction.VILLAGER)
        self.revealed = False

    # Reveal yourself as the mayor to the townspeople.
    def interact(self, other_agent):
        if randint(0, 9) < 3 and not self.revealed:
            if self.interactions:
                print("I, the Mayor[", self.unique_id, "], have revealed myself")
            self.revealed = True
        else:
            if self.interactions:
                print("I, the Mayor[", self.unique_id, "], am doing nothing")
            pass