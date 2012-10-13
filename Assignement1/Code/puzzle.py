'''NAMES OF THE AUTHOR(S):

- Florentin Rochet
- Leonard Debroux
'''

from search import *
from IO import IO
from state import State
import sys
from time import time
import Board

######################  Implement the search #######################

class PuzzleProblem(Problem):

    def __init__(self,initial = [], goal=None):
        
        self.goal = goal
        self.initial = initial
        self.numbernodes = 0
        self.parse_init(self.initial)
        Problem.__init__(self,State(self.initial))
        #move's direction allowed :
        self.direction = ["north", "south","west","east"]
    

    def goal_test(self, nodestate):
        self.numbernodes += 1
        return nodestate.state[3][1] == "1" and nodestate.state[3][2] == "1" and \
        nodestate.state[4][1] == "1" and nodestate.state[4][2] == "1"

        #return state == self.goal

        
    def successor(self, state):
        """
        Look at all the zero and for each of them, ask a move towards each direction. Return
        a couple (action, state) if the move is valid
        In this problem, each move cost 1. We don't need to specify the action since
        it's no relevant to the compute of the path cost. So successor will yield (None, state)
        """
        x = 0
        while x < len(state.state):
            y = 0
            while y < len(state.state[x]) :
                if (state.state[x][y] == "0"):
                    for direc in self.direction :
                        newState = state.move(x,y,direc)
                        if(newState):
                            #self.print_conf(newState.state)
                            yield (None,newState)
                y+=1
            y=0
            x+=1
    

    def print_conf(self, state, path=None):
        """
            print the state
        """   
        if path==None :
            for liste in state :
                for elem in liste :
                    sys.stdout.write(elem+" ")
                print("\n")
            print("\n")
        else :
            io = IO(path)
            io.init_writter()
            for liste in state :
                io.write_line(str(liste))
                io.write_line("\n")
            io.close()
            
                   
    def parse_init(self,init, path=None):
        """
        Parse a representation given to a representation of an Object State
        @see State.state
        """
        if path == None:
            path = ""
            for list in init :
                for elem in list :
                    path += elem
        Io = IO(path)
        Io.init_reader()
        init = Io.file   
        self.initial = []
        for line in init:
                linestate = []
                
                for char in line:
                    if char != " " and char != "\n":
                        linestate += char
                    
                self.initial.append(linestate)
            
            
###################### Launch the search #########################

start_time = time()

#problem=PuzzleProblem()
problem = PuzzleProblem(sys.argv[1])
#example of bfs search
#problem.print_conf(problem.initial.state)


node=breadth_first_graph_search(problem)

#node=depth_first_tree_search(problem)
#node=depth_first_graph_search(problem)


#example of print
path=node.path()
path.reverse()
i = 0
enlapsed = time() - start_time
for n in path:
    i+=1
#    print(n.state) #assume that the __str__ function of states output the correct format
#    problem.print_conf(n.state.state)
print (i, 'étapes')
print (problem.numbernodes, 'noeuds explorés')
print (enlapsed, 'seconds')



if __name__ == "__main__" :
    plateau = Board("../benchs/sokoInst01.goal")
    plateau.print_board()
        
