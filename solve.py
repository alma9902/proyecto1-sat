from z3 import *
from encode import *
from grid import *

class Solve:
    def __init__(self,height, width, steps):
        self.height = height
        self.width  = width
        self.steps  = steps
        #create grid
        self.grid   = World(self.height, self.width)
        self.grid.get_obstacles()
        self.grid.build_world()
        #create agent
        self.agent  = Agent(0,0,self.grid)


    def solution(self):
        possible_cells =[[0,0]]
        self.sat = False

        for step in range(self.steps):
            #solver
            self.solver = Solver()
            self.knowledge = Encode(self.height, self.width)
            #initial knowledge and constraints at the time
            self.knowledge.initial_knowledge(step+1)

            #get the possible_cells and update the world
            possible_cells = self.agent.get_cells(possible_cells)
            print("Casillas posibles")
            print(possible_cells)
            self.constraints(possible_cells, step+1)
            #encode and add to clauses all possibles movements with constraints and check if an agent achieved the goal
            self.move(possible_cells,step+1)
            #obstacles
            self.obstacles(possible_cells,step+1)
            #print("CLAUSES:")
            #print(And(self.knowledge.clauses))
            #add clauses to the solver
            self.solver.add(And(self.knowledge.clauses))
            if str(self.solver.check()) == 'sat':
                self.sat = True
                break;

        if self.sat:
            print("Se puede llegar a la meta en "+ str(self.steps)+ " pasos")
            print(self.solver.model())
        else:
            print("No se puede llegar a la meta en "+ str(self.steps)+ "pasos")

    def constraints(self, positions, time):
        gold = []
        for position in positions:
            gold += self.knowledge.gold(position[0],position[1], time)

        self.knowledge.clauses += self.knowledge.exactly_one_goal(gold)

    def move(self, positions,time):
        possibles = []
        constraints = []
        goals = []
        gold = []
        for position in positions:
            possibles += self.knowledge.position_agent(position[0],position[1],time)
            constraints += self.knowledge.to_move(position[0],position[1],time)
            goals += self.knowledge.goal(position[0],position[1],time)
            #check if this cell has gold
            if self.grid.world[position[0]][position[1]].gold:
                gold += self.knowledge.gold(position[0],position[1],time)
                #self.knowledge.clauses += self.knowledge.position_agent(position[0], position[1], time)
            else:
                gold += self.knowledge.not_gold(position[0],position[1],time)

        #exactly one movement per step
        #self.knowledge.clauses += [Or(possibles)]
        self.knowledge.clauses += self.knowledge.exactly_one(possibles)
        #exactly one constraint to move
        self.knowledge.clauses += self.knowledge.exactly_one(constraints)
        #exactly one goal
        self.knowledge.clauses += self.knowledge.exactly_one_goal(goals)

        #gold?
        self.knowledge.clauses += gold


    def obstacles(self, positions, time):
        obs = []
        for position in positions:
            if self.grid.world[position[0]][position[1]].obstacle:
                obs += self.knowledge.obstacle_cell(position[0],position[1],time)
            else:
                obs += self.knowledge.not_obstacle_cell(position[0],position[1],time)
        self.knowledge.clauses += obs

    def formula(self):
        for clause in self.knowledge.clauses:
            self.solver.add(clause)


solve = Solve(3,3,2)
solve.solution()
