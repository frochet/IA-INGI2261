'''NAMES OF THE AUTHOR(S): 
Debroux Léonard, Rochet Florentin'''

from search import *
from Board import Board
from State import State
from Direction import *
from IO import IO
from Box import Box
from Char import Char
from time import time
import heuristic

class Sokoban(Problem):
    """ 
        This class solve a sokoban game 
    """

    def __init__(self,filename):
        """
            filename has the form pathto/sokoInstxy 
            without the .goal or .init
            This constructor make the static board 
            and give the dynamic items (boxes, char)
            to the first state.
        """
        
        self.board = Board(filename+".goal")
        #self.board.print_board_repr()
        self.numbernodes = 0
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
        
        self.goalsize = len(self.board.positionGoal)
        self.listCombi = heuristic.make_combi(self.board.positionGoal,self.goalsize)
        self.mini = 10000
        Problem.__init__(self, State(self.board,self.boxes,self.char,[]))
    
    def goal_test(self, state):
        """
            Perform a goal test by testing 
            if the boxes' position are at the goals' position
        """
        self.numbernodes += 1

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
            No action because they are all the same, 
            each is a move in one of the
            directions. Each cost we be 1
        """
        
        #state.print_board()
        #self.board.print_board(state.char, state.boxes)
        #print (state.currentDeadStates)
        
        for direct in self.direction :
            newState = state.move(direct)
            if newState :
                yield (None, newState)
        
    def h(self,node):
        ##
        #  HEURISTIC 1 : return h(n) = 0
        #
        ###
        
        #return 0
        
        ###
        #  HEURISTIC 2 : SUM OF THE MIN OF THE MANHATTAN DISTANCE
        #
        ###
        boxes = node.state.clone_boxes(node.state.boxes)
        sums = []
        conf = []
        for goal in self.board.positionGoal:
            for box in boxes :
                sums.append(abs(box.x-goal[1])+abs(box.y-goal[0]))
            mini = 10000
            for elem in sums :
                if elem < mini :
                        mini=elem
            conf.append(mini)
            boxes.pop(sums.index(mini))
            sums = []
        val = sum(conf)
        return val

        ###
        #     HEURISTIC 3 : MIN OF THE SUM OF ALL THE CONFIGURATION FOR MANHATTAN DISTANCE
        #
        ###
#        boxes = node.state.boxes
#        sums = []
#        listToMin = []
#        i = 0
#        j = 0
#        k = 0
#        while i < len(self.listCombi) :
#            while j < self.goalsize :
#                sums.append(abs(boxes[j].y-self.listCombi[i][0])+abs(boxes[j].x-self.listCombi[i][1]))
#                i+=1
#                j+=1
#            
#            l = k*self.goalsize
#            val = 0
#            while l < (k+1)*self.goalsize :
#                val += sums[l]
#                l+=1
#            listToMin.append(val)
#            j=0
#            k+=1
#        self.mini = 10000    
#        #print(boxes)
#        #print(self.board.positionGoal)
#        #print(self.listCombi)
#        
#        #print(listToMin)
#        for elem in listToMin :
#            if elem < self.mini :
#                    self.mini=elem
#        print(self.mini)
#        return self.mini

        ###
        #
        # HEURISTIC 4 : Count the number of box not in a goal
        #
#        i = self.goalsize
#        
#        for box in node.state.boxes :
#            for coord in self.board.positionGoal :
#                if coord[0] == box.y and coord[1] == box.x : 
#                    i-=1
#        return i
    
        


###################### Launch the search #########################
    
problem=Sokoban(sys.argv[1])
#example of bfs search
start_time = time()
node=astar_graph_search(problem,problem.h)
#node=breadth_first_graph_search(problem)
#node=depth_first_graph_search(problem)
enlapsed = time() - start_time
#example of print
path=node.path()
path.reverse()
numberOfSteps = 0
for n in path:
    numberOfSteps += 1
    n.state.print_board() #assume that the __str__ function of states output the correct format
    print("")
print (enlapsed, ' seconds')
print (numberOfSteps, ' steps')
print (problem.numbernodes, ' noeuds explorés')

        
