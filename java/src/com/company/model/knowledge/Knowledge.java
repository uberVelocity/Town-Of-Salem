package com.company.model.knowledge;

import java.util.ArrayList;

// Todo: Knowledge are things that are known to be true (who the members of the Mafia are for Mafia members etc.)

public class Knowledge {
    private ArrayList<Belief> beliefs;

    public Knowledge() {
        this.beliefs = new ArrayList<>();
    }

    public Knowledge(ArrayList<Belief> beliefs) {
        this.beliefs = beliefs;
    }

    public ArrayList<Belief> getBeliefs() {
        return beliefs;
    }

    public void setBeliefs(ArrayList<Belief> beliefs) {
        this.beliefs = beliefs;
    }
}
