'''NAMES OF THE AUTHOR(S): ...'''

from search import *
import Board
import State
from Direction import *
######################  Implement the search #######################

class Sokoban(Problem):

    def __init__(self,init):
        self.board = Board(init)
        # to do
        self.char = None
        self.boxes = []
        #end to do
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

        
