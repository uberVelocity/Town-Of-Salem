package com.company.model.agents;

import java.util.logging.Level;
import java.util.logging.Logger;

public class Mobster extends Agent {

    private final static Logger LOGGER = Logger.getLogger(Mobster.class.getName());

    public Mobster(String name) {
        super(name, AgentRole.MOBSTER);
        LOGGER.log(Level.INFO, "Created mobster");
    }

    public void talk() {
        System.out.println("Mobster reporting");
    }
}
