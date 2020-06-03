from random import randint

from .agent import Villager, Role, Faction, State

class Mayor(Villager):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, Role.MAYOR, Faction.VILLAGER)
        self.revealed = False

    # Reveal yourself as the mayor to the townspeople.
    def interact(self, other_agent):
        if randint(0, 9) < 3:
            print("I, the Mayor, have revealed myself")
            self.revealed = True