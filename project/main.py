import model.agents.agent_two as agents

if __name__ == "__main__":
    # Define a new Villager agent with the 'Investigator' role.
    agent = agents.Villager('Investigator')

    # Test that the agent can talk.
    agent.talk()