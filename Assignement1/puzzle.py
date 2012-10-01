'''NAMES OF THE AUTHOR(S): ...'''

from search import *
import IO
from state import State

######################  Implement the search #######################

class PuzzleProblem(Problem):

    def __init__(self, goal=None):
        
        self.goal = goal
        self.initial = []
        self.parse_init("init_example.txt")
        Problem.__init__(State(self.initial))
        #move's direction allowed :
        self.direction = ["north", "south","west","east"]
    
    def goal_test(self, state):
        return state.state[3][1] == 1 and state.state[3][2] == 1 and \
        state.state[4][1] == 1 and state.state[4][2] == 1

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
        y = 0
        while x < len(state):
            while y < len(state[x]) :
                if (state[x][y] == "0"):
                    for direc in self.direction :
                        newState = state.move(x,y,direc)
                        if(newState):
                            yield (None,newState)
                y+=1
            x+=1
    

    def print_conf(self,state, path=None):
        """
            print the state
        """   
        if path==None :
            for liste in state :
                for elem in liste :
                    print(elem+" ")
                print("\n")
        else :
            io = IO(path)
            io.init_writter()
            for liste in state :
                for elem in liste :
                    print(elem+" ",io.file)
                print("\n",io.file)
            
                   
    def parse_init(self, path):
        """
        Parse une configuration re��ue en entr��e en une represation valide pour
        l'utilisation du programme.
        """
        IO = IO(path)
        IO.init_reader()
        
        for line in IO.file:
            linestate = []
            
            for char in line:
                if char != " ":
                    linestate += char
                
            self.initial += linestate
            
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
node=breadth_first_graph_search(problem)
#example of print
path=node.path()
path.reverse()
for n in path:
    print(n.state) #assume that the __str__ function of states output the correct format

        
