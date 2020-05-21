# Example definition of a class using 'pythonic' public variables.
import enum

from abc import ABC, abstractmethod

class Faction(enum.Enum):
    VILLAGER = 0
    MAFIOSO = 1

class Agent(ABC):

    @abstractmethod
    def __init__(self, faction, role, name = 'Townsman'):
        print('Creating a townsman!')
        self.faction = faction
        self.role = role
        self.name = name

    def talk(self):
        print(self.name, ' is talking!')

    def get_faction(self):
        return self.role

    def interact(self, agent):
        print(self.name, ' is interacting with ', agent.name, '.')

"""Villager subclass of agent."""
class Villager(Agent):
    def __init__(self, role, name = 'Villager', faction = Faction.VILLAGER):
        super().__init__(faction, role, name)
        print('I am assigned the faction of', self.faction)
        