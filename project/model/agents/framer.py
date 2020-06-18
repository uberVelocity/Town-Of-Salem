from .agent import Mobster, Role, Faction, Health

class Framer(Mobster):

    def __init__(self, unique_id, model, interactions=False):
        super().__init__(unique_id, model, Role.FRAMER, interactions, Faction.MOBSTER )

    # Picks a target and makes it appear as Mobster if inspected by Sheriff
    def interact(self, other_agent):
        if self.interactions:
            print("I, the Framer[", self.unique_id, "], am attempting to Frame ", other_agent.name)
        other_agent.visited_by.append(self)
        self.visiting = other_agent
        other_agent.framed = True

        # If Mafioso and Godfather are dead, Framer visits the target himself
        if self.agents[7].health == Health.DEAD and self.agents[5].health == Health.DEAD:
            other_agent.visited_by.append(self)
            other_agent.attacked = True

    def step(self):
        if self.is_alive():
            self.interact(self.pick_random_villager())
        pass