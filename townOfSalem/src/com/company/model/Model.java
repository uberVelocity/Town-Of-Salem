package com.company.model;

import com.company.model.agents.Agent;
import com.company.model.agents.Mobster;
import com.company.model.agents.Villager;

import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Model {

    private final static Logger LOGGER = Logger.getLogger(Model.class.getName());

    private ArrayList<Agent> agents;

    public Model(int nVillagers, int nMobsters) {
        int total = nVillagers + nMobsters;

        this.agents = initializeAgents(nVillagers, nMobsters);

        LOGGER.log(Level.INFO, "Initialized world");
        LOGGER.log(Level.INFO, "Number of agents: " + total);
    }

    /**
     * Initializes the agents of the model that will participate in the game.
     * @param numberVillagers specifies how many villagers to initialize
     * @param numberMobsters specifies how many mobsters to initialize.
     * @return list of agents.
     */
    private ArrayList<Agent> initializeAgents(int numberVillagers, int numberMobsters) {
        ArrayList<Agent> agents = new ArrayList<Agent>();
        try {
            for (int i = 0; i < numberVillagers ; i++) {
                String name = "Agent " + i;
                Agent newAgent = new Villager(name);
                agents.add(newAgent);
            }
            for (int i = 0; i < numberMobsters; i++) {
                String name = "Agent " + i;
                Agent newAgent = new Mobster(name);
                agents.add(newAgent);
            }
        }
        catch (Exception e) {
            System.out.println(e);
        }
        return agents;
    }

    public Model(ArrayList<Agent> agents) {
        this.agents = agents;
    }

    public void setAgents(ArrayList<Agent> agents) {
        this.agents = agents;
    }

    public ArrayList<Agent> getAgents() {
        return agents;
    }
}
