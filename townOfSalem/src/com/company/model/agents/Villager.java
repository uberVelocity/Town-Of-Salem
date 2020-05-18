package com.company.model.agents;

import java.util.logging.Level;
import java.util.logging.Logger;

public class Villager extends Agent {

    private final static Logger LOGGER = Logger.getLogger(Villager.class.getName());

    public Villager(String name) {
        super(name, AgentFaction.VILLAGER);
        LOGGER.log(Level.INFO, "Created a villager");
    }

    public void talk() {
        System.out.println("Villager reporting");
    }

}
