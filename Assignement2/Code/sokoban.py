'''NAMES OF THE AUTHOR(S): Florentin Rochet, Leonard Debroux'''

from search import *
from Board import Board
from State import State
from Direction import *
from IO import IO
from Box import Box
from Char import Char
######################  Implement the search #######################

class Sokoban(Problem):
    """ 
        This class solve a sokoban game 
    """

    def __init__(self,filename):
        """
            filename has the form pathto/sokoInstxy without the .goal or .init
            This constructor make the static board and give the dynamic items (boxes, char)
            to the first state.
        """
        
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
        self.direction = [Direction.UP,Direction.DOWN,Direction.LEFT,Direction.RIGHT]

        # add goal
        Problem.__init__(self, State(self.board,self.boxes,self.char,[]))
    
    def goal_test(self, state):
        """
            Perform a goal test by testing if the boxes' position are at the goals' position
        """
        i = 0
        for box in state.boxes :
            for coord in self.board.positionGoal :
                if coord[0] == box.y and coord[1] == box.x : 
                    i+=1
            if i == 0 : return False
            i = 0
        return True
            

        
    def successor(self, state):
        """
            yield the next state to a current state.
            No action because they are all the same, each is a move in one of the
            directions. Each cost we be 1
        """
        #state.print_board()
        for direct in self.direction :
            newState = state.move(direct)
            if newState :
                yield (None, newState)
        
    def h(self,node):
#        goals = self.board.positionGoal
#        boxes = node.state.boxes
#        sums = []
#        for goal in goals:
#            for box in boxes :
#                pass
        return 0
        


###################### Launch the search #########################
    
problem=Sokoban(sys.argv[1])
#example of bfs search
node=astar_graph_search(problem,problem.h)
#node=depth_first_graph_search(problem)
#example of print
path=node.path()
path.reverse()
for n in path:
    print(n.state.print_board()) #assume that the __str__ function of states output the correct format

        
