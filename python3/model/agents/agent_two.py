# Example definition of a class using 'pythonic' public variables.
class Agent:

    def __init__(self, role, name = 'Townsman'):
        self.role = role
        self.name = name

    def talk(self):
        print(self.name, ' is talking!')

    def interact(self, agent):
        print(self.name, ' is interacting with ', agent.name, '.')