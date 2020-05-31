from .agents.agent import TownAgent
from .agents.doctor import Doctor

from mesa import Model
from mesa.time import RandomActivation

class TownModel(Model):
    """A model with some number of agents."""
    def __init__(self, num_villagers, num_mobsters):
        self.init_agents(num_villagers, num_mobsters)

        self.show_agents()
        self.distributeAgents()

    # Initialize the agents of the game
    def init_agents(self, num_villagers, num_mobsters):
        self.num_agents = num_villagers + num_mobsters
        self.schedule = RandomActivation(self)  # TODO: Potentially switch to SimulatenousActivation()
        self.agents = []

        # Create agents
        temp = []
        
        # Create Doctor
        doctor = Doctor(0, self)
        temp.append(doctor)

        self.agents.append(doctor)
        self.schedule.add(doctor)

        # TODO: Change to looping through temp and adding each
        # agent one by one from there as roles are fixed in the
        # simulation. 
        for i in range(len(temp), self.num_agents):
            a = TownAgent(i, self)
            self.agents.append(a)
            self.schedule.add(a)

    # Advance the model by one step.
    def step(self):
        self.schedule.step()

    # Print all properties of all agents.
    def show_agents(self):
        for i in range(len(self.agents)):
            self.print_properties(self.agents[i])

    # Distribute agents list to all agents
    def distributeAgents(self):
        for i in range(len(self.agents)):
            self.agents[i].agents = self.agents

    # Print all properties of agent
    def print_properties(self, agent):
        print("Name: \t ", agent.name)
        print("Faction: ", agent.faction)
        print("Role: \t ", agent.role)
        print("Health:  ", agent.health)
        print("State: \t ", agent.state)
        # TODO: Visited by format
        print("--------------------\n")
