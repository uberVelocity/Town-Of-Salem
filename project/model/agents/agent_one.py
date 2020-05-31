# Example definition of a class using the @property decorator for getters and setters.
# Parent 'Agent' class that models the agents that participate in the game.
# TODO: Determine whether the usage of the @property decorator is needed.

from abc import ABC, abstractmethod

class Agent(ABC):
    """Agent constructor which initializes an agent with a role and a name.""" 
    @abstractmethod
    def __init__(self, role, name = 'Townsman'):
        self._role = role
        self._name = name

    @property
    def name(self):
        """Definition of the 'name' property."""
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @name.deleter
    def name(self):
        del self._name

    @property
    def role(self):
        """Definition of the 'role' property."""
        return self._name
    
    @role.setter
    def role(self, new_role):
        self._role = new_role

    @role.deleter
    def role(self):
        del self._role

    def talk(self):
        print(self.name, ' is talking!')

    def interact(self, agent):
        print(self.name, ' is interacting with ', agent.name, '.')

    