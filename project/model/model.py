import enum
import timeit

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

from .mlsolver.kripke_model import TownOfSalemAgents
from .mlsolver.formula import *

class Vote(enum.Enum):
    RANDOM = 0
    KNOWLEDGE = 1

class DeathStrategy(enum.Enum):
    FACTION = 0
    ALL = 1

class TownModel(Model):
    
    # A model with some number of agents.
    def __init__(self, num_villagers, num_mobsters, interactions):
        self.interactions = interactions
        self.init_agents(num_villagers, num_mobsters)

        # self.show_agents()
        self.distributeAgents()
        self.kripke_model = TownOfSalemAgents(8).ks
        self.set_init_knowledge()

    # Initialize the agents of the game.
    def init_agents(self, num_villagers, num_mobsters):
        self.num_agents = num_villagers + num_mobsters
        self.schedule = BaseScheduler(self)  # TODO: Potentially switch to SimulatenousActivation()
        self.agents = []

        # Create agents
        temp = []

        # Create Doctor
        doctor = Doctor(0, self, self.interactions)
        temp.append(doctor)

        # Create Lookout
        lookout = Lookout(1, self, self.interactions)
        temp.append(lookout)

        # Create Sheriff
        sheriff = Sheriff(2, self, self.interactions)
        temp.append(sheriff)

        # Create Mayor
        mayor = Mayor(3, self, self.interactions)
        temp.append(mayor)

        # Create Bodyguard
        bodyguard = Bodyguard(4, self, self.interactions)
        temp.append(bodyguard)

        # Create Godfather
        godfather = Godfather(5, self, self.interactions)
        temp.append(godfather)

        # Create Framer
        framer = Framer(6, self, self.interactions)
        temp.append(framer)

        # Create Mafioso
        mafioso = Mafioso(7, self, self.interactions)
        temp.append(mafioso)

        # Add agents in the model and schedule them on every model step
        for i in range(num_mobsters + num_villagers):
            self.agents.append(temp[i])
            self.schedule.add(temp[i])

        # Set initial knowledge configuration - UNCOMMENT TO EXPERIMENT
        

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
            for i, vote in enumerate(votes):
                if vote >= len(alive) / 2 + 1:
                    self.agents[i].health = Health.DEAD
                    if self.interactions:
                        print("DEAD - Linchying ", self.agents[nominee], " with ", votes[nominee], " votes")
                    break
        if self.interactions:
            print("VOTES: ", votes, "\n")
        pass

    def set_init_knowledge(self):
        agents = self.agents
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
        # self.kripke_model.print()
        
    # Updates agent's knowledge and updates kripke model
    def announce_information(self, strategy):
        agents = self.alive_agents()
        for agent in self.agents:
            for alive_agent in agents:
                if agent.faction == Faction.VILLAGER:

                    # Create fact to add to all villagers
                    if self.interactions:
                        print("I, the ", alive_agent.role, " [", alive_agent.name, "] know before addition: ", alive_agent.knowledge)
                    if strategy == DeathStrategy.FACTION:
                        fact = (agent.name, str(agent.faction.value))
                        alive_agent.knowledge.add(fact)

                        # Update kripke model correspondingly
                        atom = Atom(fact)
                        self.kripke_model = self.kripke_model.solve_a(str(alive_agent.name), atom)
                    elif strategy == DeathStrategy.ALL:
                        facts = agent.knowledge
                        for fact in facts:
                            alive_agent.knowledge.add(fact)

                            # Update kripke model correspondingly
                            atom = Atom(fact)
                            self.kripke_model = self.kripke_model.solve_a(str(alive_agent.name), atom)

                    # Update all villagers with fact
                    if self.interactions:
                        print("I, the ", alive_agent.role, " [", alive_agent.name, "] know after addition: ", alive_agent.knowledge)
        pass

    # Determine whether agent should die
    def resolve_dead(self, agent):
        if agent.attacked == True and agent.protected == False:
            agent.health = Health.DEAD
            self.announce_information(DeathStrategy.ALL)
        if agent.mafia_voted == True and self.agents[7].health == Health.DEAD:
            agent.health = Health.DEAD
            self.announce_information(DeathStrategy.ALL)
        if self.interactions:
            print("Agent ", agent.name, " visiting:", agent.visiting)
        if (agent.role == Role.MAFIOSO or agent.role == Role.GODFATHER) and (self.agents[4].visiting == agent.visiting):
            # print(agent.name, " should die!")
            agent.health = Health.DEAD
            # print("Agent ", agent.name, "'s health:", agent.health)
            self.announce_information(DeathStrategy.FACTION)
        pass

    # Prints dead agents
    def print_dead(self):
        for agent in self.agents:
            if agent.health == Health.DEAD:
                print("DEAD: ", agent.name)

    # Update knowledge of agents and kripke model with respect to Mayor's faction
    def resolve_mayor(self, agent):
        if agent.revealed == True:
            fact = (agent.name, str(Faction.VILLAGER.value))
            agents = self.alive_agents()
            for agent in agents:
                agent.knowledge.add(fact)
            
                # Update kripke model correspondingly
                atom = Atom(fact)
                self.kripke_model = self.kripke_model.solve_a(str(agent.name), atom)            
        pass

    # Determine who visited the lookout's target
    def resolve_lookout(self, agent):
        if agent.visiting.attacked and agent.visiting.protected == False and len(agent.visiting.visited_by) == 2:
            agent.visiting.visited_by.remove(agent)
            fact = (agent.visiting.visited_by[0].name, str(Faction.MOBSTER.value))
            agent.knowledge.add(fact)

            # Update kripke model correspondingly
            atom = Atom(fact)
            self.kripke_model = self.kripke_model.solve_a(str(agent.name), atom)
            if (self.interactions):
                print("I, the Lookout[", agent.unique_id, "], see that ", agent.visiting.visited_by[0].name, " is a MAFIOSO")
        if self.interactions:
            print("I, the Lookout[", agent.unique_id, "], see that ", agent.visiting.name, " is being visited by: ", agent.visiting.visited_by)
        
    # Updates knowledge of Doctor and Kripke model based on Doctor interaction with agent
    def resolve_doctor(self, agent):
        if agent.visiting.attacked:
            fact = (agent.visiting.name, str(Faction.VILLAGER.value))
            agent.knowledge.add(fact)

            # Update kripke model correspondingly
            atom = Atom(fact)
            self.kripke_model = self.kripke_model.solve_a(str(agent.name), atom)
            if self.interactions:
                print("I, the Doctor[", agent.unique_id, "], know that agent ", agent.visiting.role, "[", agent.visiting.name, "] is a villager (he was attacked).")
        pass        

    # Determine the shown faction to the sheriff
    def resolve_sheriff(self, agent):
        fact = (agent.visiting.name, str(agent.visiting.faction.value))
        agent.knowledge.add(fact)

        # Update kripke model correspondingly
        atom = Atom(fact)
        self.kripke_model = self.kripke_model.solve_a(str(agent.name), atom)

        if self.interactions:
            print("I, the Sheriff[", agent.unique_id, "], am Inspecting agent ", agent.visiting.name, " and their faction is ", agent.visiting.faction)
        pass

    # Updates knowledge of Bodyguard and Kripke model based on Bodyguard interaction with agent
    def resolve_bodyguard(self, agent):
        if agent.visiting.attacked:
            fact = (agent.visiting.name, str(Faction.VILLAGER.value))
            agent.knowledge.add(fact)

            # Update kripke model correspondingly
            atom = Atom(fact)
            self.kripke_model = self.kripke_model.solve_a(str(agent.name), atom)
            if self.interactions:
                print("I, the Bodyguard[", agent.unique_id, "], know that agent ", agent.visiting.role, "[", agent.visiting.name, "] is a villager (he was attacked).")

    # Resolve interactions of the night
    def resolve_night(self):
        if self.interactions:
            self.print_dead()
        for agent in self.agents:
            if agent.is_alive() and agent.role == Role.LOOKOUT and agent.visiting != None:
                self.resolve_lookout(agent)

            if agent.is_alive() and agent.role == Role.MAYOR and agent.visiting != None:
                self.resolve_mayor(agent)

            if agent.is_alive() and agent.role == Role.SHERIFF and agent.visiting != None:
                self.resolve_sheriff(agent)

            if agent.is_alive() and agent.role == Role.DOCTOR and agent.visiting != None:
                self.resolve_doctor(agent)

            if agent.is_alive() and agent.role == Role.BODYGUARD and agent.visiting != None:
                self.resolve_bodyguard(agent)

            # Check whether agent should die
            self.resolve_dead(agent)
        if self.interactions:
            self.print_dead()
        pass

    # Maintenance function to clear a night.
    def end_night(self):

        # Publicly announce the role of the dead agent 
        for agent in self.agents:
            if agent.announce_role == True:
                if self.interactions:
                    print("X - I, the ", agent.role, " ,[", agent.name, "] have died!")
                agent.announce_role = False

            # Set visited_by and visiting to empty
            agent.visited_by = []
            agent.visiting = None

            # Reset protected and attacked flags
            if agent.role != Role.GODFATHER:
                agent.protected = False
            agent.attacked = False
            agent.framed = False
            agent.mafia_voted = False

    # Check that either all villagers or all mobsters are dead.
    # TODO: Make this more efficient through filter / list comprehension / counter
    # that gets incremented after every death.
    def game_over(self, winner):
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
            winner[Faction.MOBSTER.value] += 1 
        if dead_mobsters == 3:
            print("TOWN WINS!")
            winner[Faction.VILLAGER.value] += 1
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
