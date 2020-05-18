package com.company.model.world;

import com.company.model.agents.Villager;

import java.util.logging.Level;
import java.util.logging.Logger;

public class World {

    private final static Logger LOGGER = Logger.getLogger(World.class.getName());

    private WorldPhase worldPhase;

    public World() {
        LOGGER.log(Level.INFO, "Generating new world.");
        this.worldPhase = WorldPhase.DISCUSSION_AND_VOTING;

    }

    public WorldPhase getWorldPhase() {
        return worldPhase;
    }

    public void setWorldPhase(WorldPhase worldPhase) {
        this.worldPhase = worldPhase;
    }
}
