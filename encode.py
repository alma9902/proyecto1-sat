from z3 import *
from itertools import combinations
from grid import *

class Encode:
    def __init__(self, height, width):
        self.height = height
        self.width  = width
        self.clauses = []

    def exactly_one(self,literals):
        c = []
        for comb in combinations(literals, 2):
            c += [Or([Not(comb[0]), Not(comb[1])])]

        return c
    def exactly_one_goal(self, goals):
        c = []
        longi = len(goals)
        for i in range(longi):
            g = [goals[i]]
            aux = goals.copy()
            aux.remove(goals[i])
            g += self.not_goal(aux)
            c += [And(g)]
        return [Or(c)]

    def not_goal(self, goals):
        c = []
        for goal in goals:
            c += [Not(goal)]
        return c


    def encode_constraints(self, time):
        #exactly one cell has gold
        cells_gold = []
        for i in range(self.height):
            for j in range(self.width):
                new_lit = Bool("G_"+str(i)+str(j)+str(time))
                cells_gold.append(new_lit)
        self.clauses += self.exactly_one(cells_gold)


    def initial_knowledge(self,time):
        #the starting cell contain no obstacle and no gold
        not_gold = Not(Bool("G_00"+str(time)))
        not_obstacle = Not(Bool("P_00"+str(time)))

        #the agent is in grid[0][0] at the time
        if time == 0:
            agent0= Bool("A_00"+str(time))
        else:
            agent0 = Not(Bool("A_00"+str(time)))

        #add clauses
        self.clauses += [not_gold]
        self.clauses += [not_obstacle]
        self.clauses += [agent0]

    def to_move(self,i,j, time):
        sufix = str(i)+str(j)+str(time)
        agent = Bool("A_"+sufix)
        not_obstacle = Not(Bool("P_"+sufix))
        move = And(agent, not_obstacle)

        return [move]


    def goal(self,i,j,time):
        ubication_agent = Bool("A_"+str(i)+str(j)+str(time))
        ubication_gold  = Bool("G_"+str(i)+str(j)+str(time))
        goal = And([ubication_agent, ubication_gold])
        return [goal]

    def gold(self, i, j, time):
        gold = Bool("G_"+str(i)+str(j)+str(time))
        return [gold]

    def not_gold(self, i, j, time):
        not_gold = Not(Bool("G_"+str(i)+str(j)+str(time)))
        return [not_gold]
    def position_agent(self, i, j, time):
        return [(Bool("A_"+str(i)+str(j)+str(time)))]

    def not_position_agent(self, i, j, time):
        not_position = Not(Bool("A_"+str(i)+str(j)+str(time)))
        return [not_position]

    def obstacle_cell(self, i, j, time):
        return [Bool("P_"+str(i)+str(j)+str(time))]

    def not_obstacle_cell(self, i, j, time):
        return [Not(Bool("P_"+str(i)+str(j)+str(time)))]
