'''NAMES OF THE AUTHOR(S): ...'''

from search import *
from IO import IO
from state import State
import sys

######################  Implement the search #######################

class PuzzleProblem(Problem):

    def __init__(self,initial = [], goal=None):
        
        self.goal = goal
        self.initial = initial
        self.parse_init("init1.txt")
        Problem.__init__(self,State(self.initial))
        #move's direction allowed :
        self.direction = ["north", "south","west","east"]
    

    def goal_test(self, nodestate):
        return nodestate.state[3][1] == "1" and nodestate.state[3][2] == "1" and \
        nodestate.state[4][1] == "1" and nodestate.state[4][2] == "1"

        #return state == self.goal

        
    def successor(self, state):
        """
        Regarde tous les z��ros dans le state et pour chaque z��ro, demande un
        mouvement vers chaque direction, envoie un couple (action, state) si
        le mouvement est valide.
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
            
                   
    def parse_init(self, path):
        """
        Parse une configuration re��ue en entr��e en une represation valide pour
        l'utilisation du programme.
        """
        Io = IO(path)
        Io.init_reader()
        
        for line in Io.file:
            linestate = []
            
            for char in line:
                if char != " " and char != "\n":
                    linestate += char
                
            self.initial.append(linestate)
            
#    def sol_format(self, nodeList):
#        """
#        Cr��e les lignes �� entrer dans le fichier solution sous forme de string
#        et les yield successivement, en ajoutant une ligne vide pour chaque
#        changement de noeud.
#        """
#        for node in nodeList:
#            
#            for line in node.state:
#                outLine = ""
#                for char in line:
#                    outLine += char
#                yield outLine
#            yield ""
#        
            
            

###################### Launch the search #########################
    
problem=PuzzleProblem()
#example of bfs search
#problem.print_conf(problem.initial.state)
node=breadth_first_graph_search(problem)
#example of print
path=node.path()
path.reverse()
i = 0
for n in path:
    i+=1
    print(n.state) #assume that the __str__ function of states output the correct format
    problem.print_conf(n.state.state)
print (i)

        
