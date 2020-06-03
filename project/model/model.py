from .agents.agent import Faction
from .agents.agent import Health

from .agents.agent import TownAgent
from .agents.doctor import Doctor
from .agents.lookout import Lookout
from .agents.sheriff import Sheriff
from .agents.mayor import Mayor
from .agents.bodyguard import Bodyguard
from .agents.mafioso import Mafioso
from .agents.framer import Framer
from .agents.godfather import Godfather

from mesa import Model
from mesa.time import RandomActivation

class TownModel(Model):
    # A model with some number of agents.
    def __init__(self, num_villagers, num_mobsters):
        
        self.init_agents(num_villagers, num_mobsters)

        # self.show_agents()
        self.distributeAgents()

    # Initialize the agents of the game.
    def init_agents(self, num_villagers, num_mobsters):
        self.num_agents = num_villagers + num_mobsters
        self.schedule = RandomActivation(self)  # TODO: Potentially switch to SimulatenousActivation()
        self.agents = []

        # Create agents
        temp = []
        
        # Create Doctor
        doctor = Doctor(0, self)
        temp.append(doctor)

        # Create Lookout
        lookout = Lookout(1, self)
        temp.append(lookout)

        # Create Sheriff
        sheriff = Sheriff(2, self)
        temp.append(sheriff)

        # Create Mayor
        mayor = Mayor(3, self)
        temp.append(mayor)

        # Create Bodyguard
        bodyguard = Bodyguard(4, self)
        temp.append(bodyguard)

        # Create Mafioso
        mafioso = Mafioso(5, self)
        temp.append(mafioso)

        # Create Framer
        framer = Framer(6, self)
        temp.append(framer)

        # Create Godfather
        godfather = Godfather(7, self)
        temp.append(godfather)

        # Add agents in the model and schedule them on every model step
        for i in range(num_mobsters + num_villagers):
            self.agents.append(temp[i])
            self.schedule.add(temp[i])

    # Advance the model by one step.
    def step(self):
        self.schedule.step()
        self.resolve_night()
        self.end_night()
        self.game_over()

    # Resolve interactions of the night.
    def resolve_night(self):
        pass

    # Maintenance function to clear a night.
    def end_night(self):
        # Set visited_by to empty.
        for agent in self.agents:
            agent.visited_by = []

    # Check that either all villagers or all mobsters are dead.
    # TODO: Make this more efficient through filter / list comprehension / counter
    # that gets incremented after every death.
    def game_over(self):
        dead_villagers = 0
        dead_mobsters = 0
        for agent in self.agents:
            if agent.is_villager():
                if not agent.is_alive():
                    dead_villagers += 1
            if agent.is_mobster():
                if not agent.is_alive():
                    dead_mobsters += 1
        return (dead_villagers == 4 | dead_mobsters == 2)
    
    # Check that model and agents refer to the same address (used for debug).
    def check_agents(self):
        for i in range(len(self.agents)):
            print(self.agents[i] == self.agents[i].agents[i])
            print(self.agents[i], " == ", self.agents[i].agents[i]) 

    # Print all properties of all agents.
    def show_agents(self):
        for i in range(len(self.agents)):
            self.print_properties(self.agents[i])

    # Distribute agents list to all agents.
    def distributeAgents(self):
        for i in range(len(self.agents)):
            self.agents[i].agents = self.agents

    # Print all properties of agent.
    def print_properties(self, agent):
        print("Name: \t ", agent.name)
        print("Faction: ", agent.faction)
        print("Role: \t ", agent.role)
        print("Health:  ", agent.health)
        print("State: \t ", agent.state)
        # TODO: Visited by format
        print("--------------------\n")
