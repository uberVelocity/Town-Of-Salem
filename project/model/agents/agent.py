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

class ActionStrategy(enum.Enum):
    RANDOM = 0
    KNOWLEDGE = 1


class TownAgent(Agent):

    # Agent that plays the game.
    def __init__(self, unique_id, model, role, interactions, faction="Default", action=ActionStrategy.RANDOM, health=Health.ALIVE):
        super().__init__(unique_id, model)
        self.interactions = interactions
        
        self.faction = faction
        self.name = unique_id
        self.role = role
        self.health = health
        self.action = action
        if self.action == "RANDOM":
            self.action = ActionStrategy.RANDOM
        elif self.action == "KNOWLEDGE":
            self.action = ActionStrategy.KNOWLEDGE

        # Set of knowledge modeled by a tuple containing (agent_id, agent_faction)
        init_knowledge = (self.name, str(self.faction.value))
        self.knowledge = set()
        self.knowledge.add(init_knowledge)
        self.beliefs = set()

        self.attacked = False
        self.protected = False
        self.framed = False
        self.announce_role = False
        self.mafia_voted = False

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
        agents = []
        if exclude_self == True:
            for agent in self.agents:
                if agent.is_alive() and agent != self:
                    agents.append(agent)
        else:
            for agent in self.agents:
                if agent.is_alive():
                    agents.append(agent)
        return agents[randint(0, len(agents) - 1)]

    # Picks a random villager from the town
    # TODO: Make this more efficient (maybe append a fixed villager list to each mafia player
    # instead of all of the agents).
    def pick_random_villager(self):
        agent = self.agents[self.get_random()]
        while (not agent.is_alive() or agent.is_mobster()):
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
            self.interact(self.pick_random_agent(True))
        pass

    # Checks if agent is villager.
    def is_villager(self):
        return self.faction == Faction.VILLAGER

    # Checks if agent is mobster.
    def is_mobster(self):
        return self.faction == Faction.MOBSTER

class Villager(TownAgent):
    """Agent that is part of the Villager faction."""
    def __init__(self, unique_id, model, role, interactions=False, faction=Faction.VILLAGER, action=ActionStrategy.RANDOM):
        super().__init__(unique_id, model, role, interactions, faction, action)


class Mobster(TownAgent):
    """Agent that is part of the Mobster faction."""
    def __init__(self, unique_id, model, role, interactions=False, faction=Faction.MOBSTER, action=ActionStrategy.RANDOM):
        super().__init__(unique_id, model, role, interactions, faction, action)