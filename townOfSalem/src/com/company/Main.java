package com.company;

import com.company.controller.Controller;
import com.company.model.agents.Agent;
import com.company.model.Model;
import com.company.view.View;

public class Main {

    public static void main(String[] args) {
        final int NUMBER_OF_VILLAGERS = 5;
        final int NUMBER_OF_MOBSTERS = 2;

        Model model = new Model(NUMBER_OF_VILLAGERS, NUMBER_OF_MOBSTERS);
        View view = new View();

        Controller controller = new Controller(model, view);

        try {
            for (Agent agent : controller.getModel().getAgents()) {
                agent.talk();
            }
        }
        catch (Exception e) {
            System.out.println(e);
        }


    }
}
