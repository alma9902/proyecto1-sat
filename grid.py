from random import seed
from random import randint
import numpy as np

class Cell:
    def __init__(self, coord_x, coord_y, visited, obstacle, gold):
        self.coord_x  = coord_x
        self.coord_y  = coord_y
        self.visited  = visited
        self.obstacle = obstacle
        self.gold     = gold

    def to_string(self):
        st = "coord x: " + str(self.coord_x) + ", coord y: " + str(self.coord_y)
        st+= ", visited : "+ str(self.visited) + ", obstacle: "+ str(self.obstacle)
        st+= ", gold : "+ str(self.gold)
        return st
class World:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.obstacles = []
        self.world =[]
        self.gold = []

    def get_obstacles(self):
        #Number of obstacles
        num_obs = randint(0, self.m*self.n-4)

        #generate coords for the obstacles
        for i in range(num_obs):
            x= randint(0,self.n-1)
            y= randint(0, self.m-1)
            if not (x == 0 and y == 0):
                self.obstacles.append([x,y])

        #generate random coords for the position of gold
        self.gold = [randint(0,self.n-1), randint(0,self.m-1)]
        while(self.gold in self.obstacles or self.gold == [0,0]):
            self.gold = [randint(0,self.n-1), randint(0,self.m-1)]

        print("Obstacles: ")
        print(self.obstacles)
        print("Gold: ")
        print(self.gold)

    def build_world(self):
        #initialize world
        for i in range(self.m):
            row = []
            for j in range(self.n):
                new_cell = Cell(i,j,False,False,False)
                row.append(new_cell)

            self.world.append(row)

        #add obstacles and gold to the World
        for o in self.obstacles:
            self.world[o[0]][o[1]] = Cell(o[0],o[1], False, True, False)

        self.world[self.gold[0]][self.gold[1]]= Cell(self.gold[0], self.gold[1], False, False, True)

    def to_string(self):
        #print state of world
        for i in self.world:
            for j in i:
                print(j.to_string())

class Agent:
    def __init__(self,coord_x,coord_y,grid):
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.grid    = grid


    def get_cells(self,cells):
        height = self.grid.m
        width  = self.grid.n
        new_cells = []
        for cell in cells:
            i = cell[0]
            j = cell[1]
            self.grid.world[i][j].visited = True
            #move to up
            if i > 0:
                #update grid
                if not self.grid.world[i-1][j].visited :
                    self.grid.world[i-1][j].visited = True
                    #add to the possible_cells
                    new_cells.append([i-1,j])
            #move to right
            if width-1 > j:
                if not self.grid.world[i][j+1].visited:
                    self.grid.world[i][j+1].visited = True
                    new_cells.append([i,j+1])
            #move to down
            if i < height-1:
                if not self.grid.world[i+1][j].visited:
                    self.grid.world[i+1][j].visited = True
                    new_cells.append([i+1,j])

        return new_cells


    def position(self):
        return "A_"+ str(coord_x) + str(coord_y)

#world = World(6,6)
#world.get_obstacles()
#world.build_world()
