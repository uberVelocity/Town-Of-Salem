from .agent import Mobster, Role, Faction

class Framer(Mobster):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, Role.FRAMER, Faction.MOBSTER)

    # Picks a target and makes it appear as Mobster if inspected by Sheriff
    def interact(self, other_agent):
        # print("I, the Framer[", self.unique_id, "], am attempting to Frame ", other_agent.name)
        other_agent.visited_by.append(self)
        self.visiting = other_agent
        other_agent.framed = True

    def step(self):
        if self.is_alive():
            self.interact(self.pick_random_villager())
        pass