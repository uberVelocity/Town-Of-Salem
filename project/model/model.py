from .agents.agent import TownAgent

from mesa import Model
from mesa.time import RandomActivation

class TownModel(Model):
    """A model with some number of agents."""
    def __init__(self, num_villagers, num_mobsters):
        self.num_agents = num_villagers + num_mobsters
        self.schedule = RandomActivation(self)
        self.agents = []

        # Create agents
        for i in range(self.num_agents):
            a = TownAgent(i, self)
            self.agents.append(a)
            self.schedule.add(a)

        self.show_agents()
        self.distributeAgents()

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()

    def show_agents(self):
        for i in range(len(self.agents)):
            print(self.agents[i].name)

    def distributeAgents(self):
        for i in range(len(self.agents)):
            self.agents[i].agents = self.agents