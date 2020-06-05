import enum

from random import randint

from .agents.agent import Faction
from .agents.agent import Health
from .agents.agent import Role

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
from mesa.time import BaseScheduler

class Vote(enum.Enum):
    RANDOM = 0
    KNOWLEDGE = 1

class TownModel(Model):
    # A model with some number of agents.
    def __init__(self, num_villagers, num_mobsters):
        
        self.init_agents(num_villagers, num_mobsters)

        # self.show_agents()
        self.distributeAgents()

    # Initialize the agents of the game.
    def init_agents(self, num_villagers, num_mobsters):
        self.num_agents = num_villagers + num_mobsters
        self.schedule = BaseScheduler(self)  # TODO: Potentially switch to SimulatenousActivation()
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

        # Create Godfather
        godfather = Godfather(5, self)
        temp.append(godfather)

        # Create Framer
        framer = Framer(6, self)
        temp.append(framer)

        # Create Mafioso
        mafioso = Mafioso(7, self)
        temp.append(mafioso)

        # Add agents in the model and schedule them on every model step
        for i in range(num_mobsters + num_villagers):
            self.agents.append(temp[i])
            self.schedule.add(temp[i])

    # Make agents vote on who to lynch
    def vote(self, strategy):

        # A random Townsman is voted to be lynched per day.
        # A majority is required to vote someone (n / 2 + 1)
        if strategy == Vote.RANDOM:
            alive = self.alive_agents()
            votes = [0] * 8
            for agent in alive:

                # Pick random alive townsman, excluding self
                nominee = alive[randint(0, len(alive) - 1)].name
                while nominee == agent:
                    nominee = alive[randint(0, len(alive) - 1)].name
                
                # Cast vote on random member
                votes[nominee] += 1 
            
            # Check for majority
            for vote in votes:
                if vote == len(alive) / 2 + 1:
                    self.agents[nominee].health = Health.DEAD
                    print("DEAD - Linchying ", self.agents[nominee], " with ", votes[nominee], " votes")
                    break
        print("VOTES: ", votes, "\n")
        pass

    # Gets the agents which are still alive
    def alive_agents(self):
        alive = []
        for i in range(0, len(self.agents)):
            if self.agents[i].health == Health.ALIVE:
                alive.append(self.agents[i]) 
        return alive

    # Advance the model by one step.
    def step(self):
        self.schedule.step()    # Allow agents to do their night actions
        self.resolve_night()    # Resolve the actions of the agents
        self.end_night()        # Reset visited_by, statuses etc
        self.vote(Vote.RANDOM)  # Vote on who to lynch during the day

    # Determine whether agent should die
    def resolve_dead(self, agent):
        if agent.attacked == True and agent.protected == False:
            agent.health = Health.DEAD
            agent.announce_role = True
        if agent.mafia_voted == True and self.agents[7].health == Health.DEAD:
            agent.health = Health.DEAD
            agent.announce_role = True
        pass

    # Determine who visited the lookout's target
    def resolve_lookout(self, agent):
        print("I, the Lookout[", agent.unique_id, "], see that ", agent.visiting.name, " is being visited by: ", agent.visiting.visited_by)
        

    # Determine the shown faction to the sheriff
    def resolve_sheriff(self, agent):
        if agent.visiting.role == Role.GODFATHER:
            print("I, the Sheriff[", agent.unique_id, "], am Inspecting agent ", agent.visiting.name, " and their faction is ", Faction.VILLAGER)
        elif agent.visiting.framed:
            print("I, the Sheriff[", agent.unique_id, "], am Inspecting agent ", agent.visiting.name, " and their faction is ", Faction.MOBSTER)
        else:
            print("I, the Sheriff[", agent.unique_id, "], am Inspecting agent ", agent.visiting.name, " and their faction is ", agent.visiting.faction)
        pass

    # Resolve interactions of the night.
    def resolve_night(self):
        for agent in self.agents:
            if agent.is_alive() and agent.role == Role.LOOKOUT:
                self.resolve_lookout(agent)

            if agent.is_alive() and agent.role == Role.SHERIFF:
                self.resolve_sheriff(agent)

            # Check whether agent should die
            self.resolve_dead(agent)
        pass

    # Maintenance function to clear a night.
    def end_night(self):

        # Publicly announce the role of the dead agent 
        for agent in self.agents:
            if agent.announce_role == True:
                print("X - I, the ", agent.role, " ,[", agent.name, "] have died!")
                agent.announce_role = False

            # Set visited_by to empty
            agent.visited_by = []

            # Reset protected and attacked flags
            if agent.role != Role.GODFATHER:
                agent.protected = False
            agent.attacked = False
            agent.framed = False
            agent.mafia_voted = False

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
        if dead_villagers == 5:
            print("MAFIA WINS!")
        if dead_mobsters == 3:
            print("TOWN WINS!")
        return (dead_villagers == 5 or dead_mobsters == 3)

    # Distribute agents list to all agents.
    def distributeAgents(self):
        for i in range(len(self.agents)):
            self.agents[i].agents = self.agents

    # Print all properties of all agents.
    def show_agents(self):
        for i in range(len(self.agents)):
            self.print_properties(self.agents[i])

    # Print all properties of agent.
    def print_properties(self, agent):
        print("Name: \t ", agent.name)
        print("Faction: ", agent.faction)
        print("Role: \t ", agent.role)
        print("Health:  ", agent.health)
        # TODO: Visited by format
        print("--------------------\n")
