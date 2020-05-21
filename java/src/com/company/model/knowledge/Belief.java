package com.company.model.knowledge;

/**
 * Todo: Formalize beliefs to include beliefs about other agents' beliefs.
 * Todo: For example I believe that agent 2 believes that agent 1 is Godfather.
 * Todo: Beliefs are things that an agent believes to be true but it is not certain that they are true.
 */
public class Belief {
    private String description;
    private String aboutWho;
}
