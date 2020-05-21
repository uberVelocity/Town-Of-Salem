package com.company.model.agents;

import com.company.model.knowledge.Knowledge;

import java.util.ArrayList;

public abstract class Agent {
    private String name = "Townsman";
    private AgentFaction role = AgentFaction.UNDEFINED;

    private ArrayList<Agent> visitors; // TODO: Think of a better way to represent interactions between Agents
    private Knowledge knowledge;

    public Agent() {}

    public Agent(String name) {
        this.name = name;
        this.knowledge = new Knowledge();
    }

    public Agent(String name, AgentFaction role) {
        this.name = name;
        this.role = role;
    }

    public void talk() {
        System.out.println(this.getName() + " is talking");
    }

    public void interact() {
        System.out.println(this.getName() + " is interacting");
    }

    public void setName(String name) {
        this.name = name;
    }

    public AgentFaction getRole() {
        return role;
    }

    public Knowledge getKnowledge() {
        return knowledge;
    }

    public void setKnowledge(Knowledge knowledge) {
        this.knowledge = knowledge;
    }

    public void setRole(AgentFaction role) {
        this.role = role;
    }

    public ArrayList<String> getFactsKnown() {
        return factsKnown;
    }

    public void setFactsKnown(ArrayList<String> factsKnown) {
        this.factsKnown = factsKnown;
    }

    public String getName() {
        return name;
    }
}
