package com.company.model;

import com.company.model.agents.Agent;
import com.company.model.agents.Mobster;
import com.company.model.agents.Villager;
import com.company.model.world.World;

import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * The model of the game. Includes the world and the agents playing.
 * Agents have knowledge and beliefs about the world.
 */
public class Model {

    private final static Logger LOGGER = Logger.getLogger(Model.class.getName());

    private ArrayList<Agent> agents;
    private World currentWorld;

    /**
     * Model constructor. Initializes the agents and the world of the game.
     * @param nVillagers number of villagers playing in the game.
     * @param nMobsters number of mobsters playing in the game.
     */
    public Model(int nVillagers, int nMobsters) {
        int total = nVillagers + nMobsters;

        this.agents = initializeAgents(nVillagers, nMobsters);

        LOGGER.log(Level.INFO, "Initialized world");
        LOGGER.log(Level.INFO, "Number of agents: " + total);

        this.currentWorld = initializeWorld();
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
            LOGGER.log(Level.SEVERE, e.toString());
        }
        return agents;
    }

    /**
     * Initializes the world of the model. Called every time a new game is initialized.
     * @return World object representing the current world of the game.
     */
    private World initializeWorld() {
        return new World();
    }

    public void setAgents(ArrayList<Agent> agents) {
        this.agents = agents;
    }

    public void setCurrentWorld(World currentWorld) {
        this.currentWorld = currentWorld;
    }

    public World getCurrentWorld() {
        return currentWorld;
    }

    public static Logger getLOGGER() {
        return LOGGER;
    }

    public ArrayList<Agent> getAgents() {
        return agents;
    }
}
