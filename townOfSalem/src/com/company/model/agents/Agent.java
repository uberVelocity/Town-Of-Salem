package com.company.model.agents;

public abstract class Agent {
    private String name = "Townsman";
    private AgentRole role = AgentRole.UNDEFINED;

    public Agent() {}

    public Agent(String name) {
        this.name = name;
    }

    public Agent(String name, AgentRole role) {
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

    public AgentRole getRole() {
        return role;
    }

    public void setRole(AgentRole role) {
        this.role = role;
    }

    public String getName() {
        return name;
    }
}
