package com.company.model.world;

import com.company.model.agents.Villager;

import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

@SuppressWarnings("InfiniteLoopStatement")
public class World {

    private final static Logger LOGGER = Logger.getLogger(World.class.getName());

    private WorldPhase worldPhase;

    /**
     * When a new game starts, a World object is created that gets initialized to the discussion and voting phase.
     */
    public World() {
        LOGGER.log(Level.INFO, "Generating new world.");
        this.worldPhase = WorldPhase.DISCUSSION_AND_VOTING;
    }

    /**
     * The main game loop that cycles through each phase of the game and performs each phase after the game has been
     * initialized.
     */
    public void gameCycle() {
        Scanner input = new Scanner(System.in);
        try {
            while (true) {
                System.out.println("Current phase: " + this.worldPhase.toString() + ". (enter)");
                input.nextLine();
                nextWorldPhase();
            }
        }
        catch (Exception e) {
            LOGGER.log(Level.SEVERE, e.toString());
        }
    }

    /**
     * Sets the current world phase to the next world phase of the game. This closely follows the standard rules of the
     * game.
     */
    public void nextWorldPhase() {
        switch (this.worldPhase) {
            case DISCUSSION_AND_VOTING -> this.worldPhase = WorldPhase.DEFENSE_AND_JUDGEMENT;
            case DEFENSE_AND_JUDGEMENT -> this.worldPhase = WorldPhase.NIGHT;
            case NIGHT -> this.worldPhase = WorldPhase.DISCUSSION_AND_VOTING;
            default -> LOGGER.log(Level.WARNING, "Invalid world state");
        }
    }

    public WorldPhase getWorldPhase() {
        return worldPhase;
    }

    public void setWorldPhase(WorldPhase worldPhase) {
        this.worldPhase = worldPhase;
    }
}
