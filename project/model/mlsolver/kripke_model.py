""" Three wise men puzzle

Module contains data model for three wise men puzzle as Kripke strukture and agents announcements as modal logic
formulas
"""
from itertools import permutations
from .kripke import KripkeStructure, World
from .formula import Atom, And, Not, Or, Box_a, Box_star
from bisect import bisect_left
from itertools import *

def add_symmetric_edges(relations):
    """Routine adds symmetric edges to Kripke frame
    """
    result = {}
    for agent, agents_relations in relations.items():
        result_agents = agents_relations.copy()
        for r in agents_relations:
            x, y = r[1], r[0]
            result_agents.add((x, y))
        result[agent] = result_agents
    return result


def add_reflexive_edges(worlds, relations):
    """Routine adds reflexive edges to Kripke frame
    """
    result = {}
    for agent, agents_relations in relations.items():
        result_agents = agents_relations.copy()
        for world in worlds:
            result_agents.add((world.name, world.name))
            result[agent] = result_agents
    return result


class TownOfSalemAgents:
    knowledge_base = []
    agents = []

    def __init__(self,n):
        self.build_agents(n)
        #print("Agents: ",self.agents)
        self.build_worlds(n)
        worlds = self.build_worlds(n)
        #print("Worlds:", worlds)

        kripke_worlds = []

        for world in worlds:
            kripke_worlds.append(World(world, worlds[world]))
        relations={}
        for i in range(n):
            id = str(i)
            relations[id]=[]
        for world in worlds:
            formulas = worlds[world]
            for i in range(n): 
                if i < 5:
                    #check if the role(villager) in current world is the same as in new world and if yes add a relation
                    for formula in formulas:
                        if (formula[0]) == i:
                            current_role = formula[1]
                    id =str(i)
                    if current_role=='0':
                        for other_world in worlds:
                            formulas2 = worlds[other_world]
                            for formula in formulas2:
                                if (formula[0]) == i:
                                    new_role = formula[1]
                        
                            if (current_role==new_role):
                                relations[id].append((world,other_world))
        relations['7'].append(('00000111','00000111'))
        relations['5'].append(('00000111','00000111'))
        relations['6'].append(('00000111','00000111'))
        for r in relations:
            relations[r] = set(relations[r])
        #print("Relations:")
        self.ks = KripkeStructure(kripke_worlds, relations)


    def print_relations(self):
        print("Relations left:")
        for agent in self.ks.relations.keys():
            print("Agent", agent, ":", self.ks.relations[agent])

                
    def extract_knowledge(self, agent_id):
            for relation in self.ks.relations:
                print(relation)
    
    def build_agents(self, n):
        for i in range(n):
            self.agents.append(str(i))


    def build_worlds(self,n):
        worlds = []
        worlds_dict = {}
        perms = self.possible_worlds()
        for i in perms:
            name = map(str,i)
            name=''.join(name)             
            worlds_dict[name] = {(idx,f):True for idx,f in enumerate(name)}
        return worlds_dict

    def nameToDict(self,name):
        temp_dict=set()
        for idx,word in enumerate(name):
             temp_dict.add(str(idx)+word+':True')
        return temp_dict



    def possible_worlds(self):
        a = list(product([0,1],repeat=8))
        worlds = []
        for i in a:
            #Filter the worlds that have only 3 mafia
            if sum(i)==3:
                worlds.append(i)
        return worlds