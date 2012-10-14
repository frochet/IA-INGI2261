'''NAMES OF THE AUTHOR(S): ...'''

from search import *
import Board
import State
from Direction import *
import IO
import Box
import Char
######################  Implement the search #######################

class Sokoban(Problem):

    def __init__(self,filename):
        self.board = Board(filename+".goal")
        Io = IO(filename+".init")
        Io.init_reader()
        self.boxes = []
        i = 0
        j = 0
        for line in Io.file :
            for elem in line :
                if elem == "$" :
                    self.boxes.append(Box(i,j))
                elif elem == "@":
                    self.char = Char(i,j)
                j+=1
            j=0
            i+=1

        # add goal
        Problem.__init__(self, State(self.board,self.boxes,self.char))
        self.direction = [Direction.UP,Direction.Down,Direction.LEFT,Direction.RIGHT]
    
    def goal_test(self, state):
        pass

        
    def successor(self, state):
        pass
        




###################### Launch the search #########################
    
problem=Sokoban(sys.argv[1])
#example of bfs search
node=breadth_first_graph_search(problem)
#example of print
path=node.path()
path.reverse()
for n in path:
    print(n.state) #assume that the __str__ function of states output the correct format

        
