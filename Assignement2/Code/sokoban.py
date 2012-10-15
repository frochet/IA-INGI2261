'''NAMES OF THE AUTHOR(S): ...'''

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
    """

    def __init__(self,filename):
        """
            
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
        i = 0
        for box in state.boxes :
            for coord in self.board.positionGoal :
                if coord[0] == box.x and coord[1] == box.y : 
                    i+=1
            
            if i == 0 : return False
            i = 0
        return True
            

        
    def successor(self, state):
        """
            No action because they are all the same, each is a move in one of the
            directions. Each cost we be 1
        """
        state.print_board()
        print (state.currentDeadStates)
        print (state.representation)
        for direct in self.direction :
            newState = state.move(direct)
            if newState :
                count = 0
                x = 0
                while x < 10:
                    if newState.boxes[0].y == 1 and newState.boxes[0].x == x:
                        count += 1
                    if newState.boxes[1].y == 1 and newState.boxes[1].x == x:
                        count += 1
                    x += 1
                if count == 2:
                    print("oups")
                #newState.print_board()
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
#node=astar_graph_search(problem,problem.h)
node=depth_first_graph_search(problem)
print(node == None)
#example of print
path=node.path()
path.reverse()
for n in path:
    print(n.state.print_board()) #assume that the __str__ function of states output the correct format

        
