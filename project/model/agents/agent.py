import enum

from abc import ABC, abstractmethod
from random import randint
from mesa import Agent

class Role(enum.Enum):
    DOCTOR = 0
    LOOKOUT = 1
    SHERIFF = 2
    MAYOR = 3
    BODYGUARD = 4
    GODFATHER = 5
    MAFIOSO = 6
    FRAMER = 7

class Faction(enum.Enum):
    VILLAGER = 0
    MOBSTER = 1

class Health(enum.Enum):
    DEAD = 0
    ALIVE = 1

class TownAgent(Agent):

    # Agent that plays the game.
    def __init__(self, unique_id, model, role="Default", faction="Default", health=Health.ALIVE):
        super().__init__(unique_id, model)
        self.faction = faction
        self.name = unique_id
        self.role = role
        self.health = health
        
        self.attacked = False
        self.protected = False
        self.framed = False
        self.announce_role = False

        self.agents = []
        self.visited_by = []
        self.visiting = None

    # Interact with other_agent depending on self.role
    # TODO: Include a strategy parameter that specifies the interaction strategy.
    def interact(self, other_agent):
        if not other_agent.is_alive():
            print('Cannot interact with dead agent.')
        else:
            print('I, agent ', self.name, ' am interacting with agent ', other_agent.name)

    # Gets a random agent that is alive from the game. Exclude self picks agent that is not themself.
    def pick_random_agent(self, exclude_self):
        agent = self.agents[self.get_random()]
        if not self.is_alive() | exclude_self:
            while agent == self or not agent.is_alive():
                agent = self.agents[self.get_random()]
        return agent

    # Picks a random villager from the town
    # TODO: Make this more efficient (maybe append a fixed villager list to each mafia player
    # instead of all of the agents).
    def pick_random_villager(self):
        agent = self.agents[self.get_random()]
        while (agent.is_mobster() or not agent.is_alive()):
            agent = self.agents[self.get_random()]
        return agent

    # Returns random integer between 0 and the number of agents - 1.
    def get_random(self):
        return randint(0, len(self.agents) - 1)

    # Debug function used to print the agent's name.
    def talk(self):
        if self.is_alive():
            print('Agent ', self.name, ' is talking.')
        else:
            print('Agent ', self.name, ' is dead.')

    # Returns whether agent is alive
    def is_alive(self):
        return self.health == Health.ALIVE
    
    # The step each agent does during the game.
    def step(self):
        # Night phase: the agent chooses another agent to interact with.
        if self.is_alive():
            self.interact(self.pick_random_agent(1))
        pass

    # Checks if agent is villager.
    def is_villager(self):
        return self.faction == Faction.VILLAGER

    # Checks if agent is mobster.
    def is_mobster(self):
        return self.faction == Faction.MOBSTER

class Villager(TownAgent):
    """Agent that is part of the Villager faction."""
    def __init__(self, unique_id, model, role, faction=Faction.VILLAGER):
        super().__init__(unique_id, model, role, faction)

class Mobster(TownAgent):
    """Agent that is part of the Mobster faction."""
    def __init__(self, unique_id, model, role, faction=Faction.MOBSTER):
        super().__init__(unique_id, model, role, faction)

