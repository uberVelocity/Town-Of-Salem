from model.agents import agent
from model.agents import agent_two

if __name__ == "__main__":
    ag = agent.Agent('Mafioso')
    ag2 = agent_two.Agent('Villager')

    ag.talk()
    ag2.talk()