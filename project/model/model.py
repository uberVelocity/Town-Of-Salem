import enum
import timeit

from model import params

from copy import copy

from math import floor

from random import randint
from random import choice

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
    # Each agent votes randomly on another agent
    RANDOM = 0

    # Villagers vote on a random person from a subset that excludes known villagers
    # Mafia vote on random villagers (uncoordinated)
    KNOWLEDGE_NO_COOP = 1
    KNOWLEDGE_VOTE_AGAINST_MAFIA = 2

class DeathStrategy(enum.Enum):
    FACTION = 0
    ALL = 1

class TownModel(Model):
    
    # A model with some number of agents.
    def __init__(self, num_villagers, num_mobsters, interactions):
        self.infer = params.infer
        if self.infer == "OFF":
            self.infer = False
        else:
            self.infer = True
        self.interactions = interactions
        self.action = params.strategy_action
        self.strategy_vote = params.strategy_vote
        if self.strategy_vote == "RANDOM":
            self.strategy_vote = Vote.RANDOM
        elif self.strategy_vote == "KNOWLEDGE_NO_COOP":
            self.strategy_vote = Vote.KNOWLEDGE_NO_COOP
        elif self.strategy_vote == "KNOWLEDGE_VOTE_AGAINST_MAFIA":
            self.strategy_vote = Vote.KNOWLEDGE_VOTE_AGAINST_MAFIA
        
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
        doctor = Doctor(0, self, self.interactions, self.action)
        temp.append(doctor)

        # Create Lookout
        lookout = Lookout(1, self, self.interactions, self.action)
        temp.append(lookout)

        # Create Sheriff
        sheriff = Sheriff(2, self, self.interactions, self.action)
        temp.append(sheriff)

        # Create Mayor
        mayor = Mayor(3, self, self.interactions)
        temp.append(mayor)

        # Create Bodyguard
        bodyguard = Bodyguard(4, self, self.interactions, self.action)
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

    # Gets alive villagers
    def get_alive_villagers(self):
        villagers = []
        for agent in self.agents:
            if agent.faction == Faction.VILLAGER:
                if agent.is_alive():
                    villagers.append(agent)
        return villagers

    # Make agents vote on who to lynch
    # A majority is required to vote someone >= (n / 2 + 1)
    def vote(self, strategy):
        alive = self.alive_agents()
        votes = [0] * 8
        # A random Townsman is voted to be lynched per day.
        if strategy == Vote.RANDOM:
            for agent in alive:

                # Pick random alive townsman, excluding self
                nominee = alive[randint(0, len(alive) - 1)].name
                while nominee == agent:
                    nominee = alive[randint(0, len(alive) - 1)].name
                
                # Cast vote on random member
                if agent.role == Role.MAYOR:
                    if agent.revealed:
                        votes[nominee] += 2
                if self.interactions:
                    print("I, [", agent.unique_id, "], voted  ", nominee, " to be lynched.")

                votes[nominee] += 1 
        elif strategy == Vote.KNOWLEDGE_NO_COOP:
            for agent in alive:
                potential_agents = copy(alive)
                
                # Villager KNOWLEDGE_NO_COOP strategy
                if agent.faction == Faction.VILLAGER:
                    for id, faction in agent.knowledge:
                        if faction == str(Faction.VILLAGER.value) and self.agents[id].is_alive():
                            potential_agents.remove(self.agents[id])
                    
                    # Pick random alive townsman, excluding self
                    if len(potential_agents) != 0:
                        nominee = potential_agents[randint(0, len(potential_agents) - 1)].name
                        while nominee == agent:
                            nominee = potential_agents[randint(0, len(potential_agents) - 1)].name

                        votes[nominee] += 1
                        if self.interactions:
                            print("I, [", agent.unique_id, "], voted  ", nominee, " to be lynched. List of potential agents:",potential_agents)
                
                # Mafia KNOWLEDGE_NO_COOP strategy
                if agent.faction == Faction.MOBSTER:
                    villagers = self.get_alive_villagers()
                    if len(villagers) != 0:
                        nominee = choice(villagers)
                        nominee = nominee.name
                        if agent.role == Role.MAYOR:
                            if agent.revealed:
                                votes[nominee] += 2
                        votes[nominee] += 1
                        if self.interactions:
                            print("I, [", agent.unique_id, "], voted  ", nominee, " to be lynched.List of potential agents:",villagers)
            
        elif strategy == Vote.KNOWLEDGE_VOTE_AGAINST_MAFIA:
            
            for agent in alive:
                potential_agents = copy(alive)
                known_mafia = []
                # Villager KNOWLEDGE_VOTE_AGAINST_MAFIA strategy
                if agent.faction == Faction.VILLAGER:
                    for id, faction in agent.knowledge:
                        if faction == str(Faction.VILLAGER.value) and self.agents[id].is_alive():
                            potential_agents.remove(self.agents[id])
                        elif faction == str(Faction.MOBSTER.value) and self.agents[id].is_alive():
                            known_mafia.append(self.agents[id])
                    
                    # Pick random alive townsman, excluding self
                    if len(known_mafia) != 0:
                        nominee = known_mafia[randint(0, len(known_mafia) - 1)].name
                        if agent.role == Role.MAYOR:
                            if agent.revealed:
                                votes[nominee] += 2
                        votes[nominee] += 1
                    elif len(potential_agents) != 0:
                        nominee = potential_agents[randint(0, len(potential_agents) - 1)].name
                        while nominee == agent:
                            nominee = potential_agents[randint(0, len(potential_agents) - 1)].name
                        if agent.role == Role.MAYOR:
                            if agent.revealed:
                                votes[nominee] += 2
                        votes[nominee] += 1
                    if self.interactions:
                        if len(known_mafia) == 0:
                            print("I, [", agent.unique_id, "], voted  ", nominee, " to be lynched. List of potential agents:",potential_agents)
                        elif len(known_mafia) != 0 :
                            print("I, [", agent.unique_id, "], voted  ", nominee, " to be lynched. List of known mafia:",known_mafia)
                
                # Mafia KNOWLEDGE_NO_COOP strategy
                if agent.faction == Faction.MOBSTER:
                    villagers = self.get_alive_villagers()
                    if len(villagers) != 0:
                        nominee = choice(villagers)
                        nominee = nominee.name

                        votes[nominee] += 1
                        if self.interactions:
                            print("I, [", agent.unique_id, "], voted  ", nominee, " to be lynched.List of potential agents:",villagers)
            pass

        # Check for majority
        for i, vote in enumerate(votes):
            if vote >= floor(len(alive) / 2) + 1:
                self.agents[i].health = Health.DEAD
                if self.interactions:
                    print("DEAD - Linchying ", self.agents[nominee], " with ", votes[nominee], " votes")
                break
        if self.interactions:
            print("VOTES: ", votes, "\n")
        pass

    def set_init_knowledge(self):
        fact = (6,'1')
        for agent in self.alive_agents():
            agent.knowledge.add(fact)
            atom = Atom(fact)
            self.kripke_model = self.kripke_model.solve_a(str(agent.name), atom)
        pass

    # Gets the agents which are still alive
    def alive_agents(self):
        alive = []
        for i in range(0, len(self.agents)):
            if self.agents[i].health == Health.ALIVE:
                alive.append(self.agents[i]) 
        return alive

    def get_alive_mafia(self):
        mafia = []
        for agent in self.agents:
            if agent.faction == Faction.MOBSTER:
                if agent.is_alive():
                    mafia.append(agent)
        return mafia

    # Advance the model by one step.
    def step(self):
        self.schedule.step()    # Allow agents to do their night actions
        self.resolve_night()    # Resolve the actions of the agents
        self.end_night()        # Reset visited_by, statuses etc
        if self.infer:
            self.infer_knowledge()
        if len(self.get_alive_villagers()) != 0 and len(self.get_alive_mafia()) != 0:
            self.vote(self.strategy_vote)  # Vote on who to lynch during the day
        # self.kripke_model.print()
        
    # Updates agent's knowledge and updates kripke model
    def announce_information(self, strategy,dead_agent):
        for agent in self.agents:
            if dead_agent.faction == Faction.VILLAGER:
                # Create fact to add to all agents
                if self.interactions:
                    print("I, the ", agent.role, " [", agent.name, "] know before addition: ", agent.knowledge)
                if strategy == DeathStrategy.FACTION:
                    fact = (dead_agent.name, str(dead_agent.faction.value))
                    agent.knowledge.add(fact)

                    # Update kripke model correspondingly
                    atom = Atom(fact)
                    self.kripke_model = self.kripke_model.solve_a(str(agent.name), atom)
                elif strategy == DeathStrategy.ALL:
                    facts = dead_agent.knowledge
                    for fact in facts:
                        agent.knowledge.add(fact)

                        # Update kripke model correspondingly
                        atom = Atom(fact)
                        self.kripke_model = self.kripke_model.solve_a(str(agent.name), atom)

                # Update all villagers with fact
                if self.interactions:
                    print("I, the ", agent.role, " [", agent.name, "] know after addition: ", agent.knowledge)
            elif dead_agent.faction == Faction.MOBSTER:
                if self.interactions:
                    print("I, the ", agent.role, " [", agent.name, "] know before addition: ", agent.knowledge)

                fact = (dead_agent.name, str(dead_agent.faction.value))
                agent.knowledge.add(fact)

                # Update kripke model correspondingly
                atom = Atom(fact)
                self.kripke_model = self.kripke_model.solve_a(str(agent.name), atom)
                if self.interactions:
                    print("I, the ", agent.role, " [", agent.name, "] know after addition: ", agent.knowledge)

        pass

    # Determine whether agent should die
    def resolve_dead(self, agent):
        if agent.attacked == True and agent.protected == False:
            agent.health = Health.DEAD
            self.announce_information(DeathStrategy.ALL,agent)
        if agent.mafia_voted == True and self.agents[7].health == Health.DEAD:
            agent.health = Health.DEAD
            self.announce_information(DeathStrategy.ALL,agent)
        if self.interactions:
            print("Agent ", agent.name, " visiting:", agent.visiting)
        if (agent.role == Role.MAFIOSO or agent.role == Role.GODFATHER) and (self.agents[4].visiting == agent.visiting):
            agent.health = Health.DEAD
            self.announce_information(DeathStrategy.FACTION,agent)
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

    def infer_knowledge(self):
        formulas = {(0,'0'),(0,'1'),(1,'0'),(1,'1'),(2,'0'),(2,'1'),(3,'0'),(3,'1'),(4,'0'),(4,'1'),
        (5,'0'),(5,'1'),(6,'0'),(6,'1'),(7,'0'),(7,'1')}
        for agent in self.alive_agents():
            if agent.faction == Faction.VILLAGER:
                for formula in formulas:
                    id, faction = formula
                    evaluate = True
                    for relation in self.kripke_model.relations[str(agent.name)]:
                        world1 , world2 = relation
                        if world1[id]!= faction or world2[id]!= faction:
                            evaluate = False
                            break
                    
                    if evaluate and (not (formula in agent.knowledge)):
                        if self.interactions:
                            print("Added formula",formula,"to knowledge of agent ",agent.name)
                        agent.knowledge.add(formula)


    
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
