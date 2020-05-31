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

class State(enum.Enum):
    NEUTRAL = 0
    ATTACKED = 1
    PROTECTED = 2

class TownAgent(Agent):
    """Agent that plays the game."""
    
    def __init__(self, unique_id, model, faction="Default", role="Default", health=Health.ALIVE, state=State.NEUTRAL):
        super().__init__(unique_id, model)
        self.faction = faction
        self.name = unique_id
        self.role = role
        self.health = health
        self.state = state
        self.agents = []
        self.visited_by = []

    # Interact with other_agent depending on self.role
    # TODO: Include a strategy parameter that specifies the interaction strategy.
    def interact(self, other_agent):
        print('I, agent ', self.name, ' am interacting with agent ', other_agent.name)

    # Gets a random agent from the game, excluding themself.
    def pick_random_agent(self, exclude_self):
        agent = self.agents[self.get_random()]
        if exclude_self:
            while agent == self:
                agent = self.agents[self.get_random()]
        return agent

    # Returns random integer between 0 and the number of agents - 1.
    def get_random(self):
        return randint(0, len(self.agents) - 1)

    # Debug function used to print the agent's name.
    def talk(self):
        if self.state == Health.ALIVE:
            print('Agent ', self.name, ' is talking.')
        else:
            print('Agent ', self.name, ' is dead.')

    # The step each agent does during the game.
    def step(self):
        # Night phase: the agent chooses another agent to interact with.
        self.interact(self.pick_random_agent(1))
        pass

class Villager(TownAgent):
    """Agent that is part of the Villager faction."""
    def __init__(self, unique_id, model, role, faction=Faction.VILLAGER):
        super().__init__(unique_id, model, faction, role)

class Mobster(TownAgent):
    """Agent that is part of the Mobster faction."""
    def __init__(self, unique_id, model, role, faction=Faction.MOBSTER):
        super().__init__(unique_id, model, faction ,role)

