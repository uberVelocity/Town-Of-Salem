""" Three wise men puzzle

Module contains data model for three wise men puzzle as Kripke strukture and agents announcements as modal logic
formulas
"""
from itertools import permutations
from .kripke import KripkeStructure, World
from .formula import Atom, And, Not, Or, Box_a, Box_star
from bisect import bisect_left
from itertools import *


class WiseMenWithHat:
    """
    Class models the Kripke structure of the "Three wise men example.
    """

    knowledge_base = []

    def __init__(self):
        worlds = [
            World('RWW', {'1:R': True, '2:W': True, '3:W': True}),
            World('RRW', {'1:R': True, '2:R': True, '3:W': True}),
            World('RRR', {'1:R': True, '2:R': True, '3:R': True}),
            World('WRR', {'1:W': True, '2:R': True, '3:R': True}),

            World('WWR', {'1:W': True, '2:W': True, '3:R': True}),
            World('RWR', {'1:R': True, '2:W': True, '3:R': True}),
            World('WRW', {'1:W': True, '2:R': True, '3:W': True}),
            World('WWW', {'1:W': True, '2:W': True, '3:W': True}),
        ]

        relations = {
            '1': {('RWW', 'WWW'), ('RRW', 'WRW'), ('RWR', 'WWR'), ('WRR', 'RRR')},
            '2': {('RWR', 'RRR'), ('RWW', 'RRW'), ('WRR', 'WWR'), ('WWW', 'WRW')},
            '3': {('WWR', 'WWW'), ('RRR', 'RRW'), ('RWW', 'RWR'), ('WRW', 'WRR')}
        }

        relations.update(add_reflexive_edges(worlds, relations))
        relations.update(add_symmetric_edges(relations))

        self.ks = KripkeStructure(worlds, relations)

        # Wise man ONE does not know whether he wears a red hat or not
        self.knowledge_base.append(And(Not(Box_a('1', Atom('1:R'))), Not(Box_a('1', Not(Atom('1:R'))))))

        # This announcement implies that either second or third wise man wears a red hat.
        self.knowledge_base.append(Box_star(Or(Atom('2:R'), Atom('3:R'))))

        # Wise man TWO does not know whether he wears a red hat or not
        self.knowledge_base.append(And(Not(Box_a('2', Atom('2:R'))), Not(Box_a('2', Not(Atom('2:R'))))))

        # This announcement implies that third men has be the one, who wears a red hat
        self.knowledge_base.append(Box_a('3', Atom('3:R')))

class TheShipThreeAgents:
    """
    Class models the Kripke structure of the The Ship for three agents (somewhat trivial).
    """
    # The knowledge_base is as of yet unused for this class
    knowledge_base = []

    def __init__(self):
        # There are only two possible configurations of killer-targer pairs
        # Note that world 231, for example, stands for the world where 1 targets 2, 2 targets 3, 3 targets 1
        worlds = [
            World('231', {'t12': True, 't23': True, 't31': True}),
            World('312', {'t13': True, 't21': True, 't32': True}),
        ]
        # In the 3-agent case, from each world only the world itself is accessible for each agents
        relations = {
            '1': {('231','231'), ('312', '312')},
            '2': {('231','231'), ('312', '312')},
            '3': {('231','231'), ('312', '312')}
        }
        # Build the Kripke model and store it in ks
        self.ks = KripkeStructure(worlds, relations)

class TheShipNAgents:
    # The knowledge_base is as of yet unused for this class
    knowledge_base = []
    agents = []

    def __init__(self, n):
        self.build_agents(n)
        print("Agents: ", self.agents)
        worlds, propositions = self.build_worlds(n)
        #print("Worlds:", worlds)

        kripke_worlds = []

        self.propositions = propositions
        #print("Propositions:", propositions)
        #print()

        # create World objects for the Kripke structure
        for world in worlds:
            kripke_worlds.append(World(world, worlds[world]))

        # initialize the agent world relations
        relations = {}
        for i in range(n):
            id = str(i)
            relations[id] = []

        for world in worlds:
            print('WOLRD=======',world)
            for i in range(n):
                id = str(i)

                # if the agent has no murderer in a world, the agent cannot possibly access this world (because the
                # agent is dead in this case)
                if (id not in world):
                    continue


                # an agent only has an accessibility relation to a world where their target is the same
                # find the current agent's target
                formulas = worlds[world]
                for formula in formulas:
                    if(formula[0]) == str(i):
                        break
                # look for other worlds where the agent has the same target
                for other_world in worlds:
                    if(formula in worlds[other_world] and id in other_world):
                        relations[id].append((world,other_world))


        for r in relations:
            relations[r] = set(relations[r])
        #print("Relations:")
        self.ks = KripkeStructure(kripke_worlds, relations)
        #print(self.ks.relations)

    def build_agents(self, n):
        for i in range(n):
            self.agents.append(str(i))

    # if proposition is true for an agent in all worlds accessible
    # from the real world, add it to the agent's knowledge base
    def add_knowledge(self, agent, world, proposition):
        """
        f = Box_a(str(agent.unique_id), Atom(proposition))
        if(f.semantic(self.ks, world.name)):
            agent.kb.append(proposition)
        """

    def update_structure(self, agents):
        print("Updating kripke structure:")
        for agent in agents:
            print(agent, " kb: ", agent.kb)
            if (agent.alive):
                for formula in agent.kb:
                    # formula only has to be evaluated once ( prop not evaluated yet? -> False)
                    if (agent.kb[formula][1] == False):
                        if("v" in formula):
                            formula_list = formula.split("v")
                            f1 = Atom(formula_list[0])
                            f2 = Atom(formula_list[1])
                            final_formula = Or(f1,f2)
                            for i in range(len(formula_list) - 2):
                                f = Atom(formula_list[i + 2])
                                final_formula = Or(final_formula, f)
                        else:
                            f = Atom(formula)
                        # if the formula in the agent's knowledge base is false, negate the formula
                        if(agent.kb[formula][0] == False):
                            f = Not(Atom(formula))
                        self.ks = self.ks.solve_a(str(agent.unique_id), f)
                        # set formula to True, so that it's not going to be evaluated again in the structure update
                        agent.kb[formula][1] = True

        #self.print_relations()

    def print_relations(self):
        print("Relations left:")
        for agent in self.ks.relations.keys():
            print("Agent", agent, ":", self.ks.relations[agent])
        N_rels = 0
        for agent in self.ks.relations.keys():
            N_rels += len(self.ks.relations[agent])
        print("Amount of relations left:", N_rels)


    def build_worlds(self, n):
        worlds = []
        worlds_dict = {}
        targets = []
        target_count = [0] * len(self.agents)
        agent_pairs = []
        perms = permutations(self.agents, 2)
        #worlds = combinations(worlds, n)
        for p in perms:
            agent_pairs.append(''.join(list(p)))

        worlds = self.combine_agent_pairs(agent_pairs, worlds, targets, target_count, n)

        for w in worlds:
            print(w)

        for w in worlds:
            name = ''.join([char[-1] for char in w])
            worlds_dict[name] = {f: True for f in w}

        print("Total amount of worlds: ", len(worlds))

        return worlds_dict, agent_pairs

    def combine_agent_pairs(self, agent_pairs, worlds, targets, target_count, n):
        """
        This function recursively builds up all possible worlds.

        :param agent_pairs: the possible killer-target pairs that are still allowed
        :param worlds: the set of worlds that are already built
        :param targets: a set of killer-target pairs
        :param n: how many agents still need to be assigned a target
        :return: a list of all possible worlds
        """
        if n == 0:
            targets = sorted(targets)
            if targets not in worlds:
                worlds.append(targets)

            return worlds

        for pair in agent_pairs:
            idx = int(pair[1])

            worlds = self.combine_agent_pairs(self.update_agent_pairs(agent_pairs, pair, target_count[idx] + 1), worlds, targets + [pair],
                                              self.increment_target_count(target_count, idx), n - 1)

        return worlds

    def update_agent_pairs(self, agent_pairs, a, count):
        return [c for c in agent_pairs if not (c[0] == a[0] or c[1] == a[1] or (c[0] == a[1] and c[1] == a[0]))]

    def increment_target_count(self, target_count, idx):
        new_target_count = [i for i in target_count]
        new_target_count[idx] += 1
        return new_target_count

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
        #print(self.ks.relations)
                        
                        


                    
                    

        #self.propositions = propositions
        #print("Propositions:", propositions)

    def print_relations(self):
        print("Relations left:")
        for agent in self.ks.relations.keys():
            print("Agent", agent, ":", self.ks.relations[agent])


    
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