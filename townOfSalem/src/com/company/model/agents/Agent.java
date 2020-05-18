package com.company.model.agents;

public abstract class Agent {
    private String name = "Townsman";
    private AgentAffinity role = AgentAffinity.UNDEFINED;

    public Agent() {}

    public Agent(String name) {
        this.name = name;
    }

    public Agent(String name, AgentAffinity role) {
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

    public AgentAffinity getRole() {
        return role;
    }

    public void setRole(AgentAffinity role) {
        this.role = role;
    }

    public String getName() {
        return name;
    }
}
