'''NAMES OF THE AUTHOR(S): ...'''

from search import *
import IO
from state import State

######################  Implement the search #######################

class PuzzleProblem(Problem):

    def __init__(self, goal):
        """ 
        goal to be precised 
        """
        self.initial = {}
        self.parse_init()
        Problem.__init__(State(self.initial), goal)
        pass

    
    def goal_test(self, state):
        pass

        
    def successor(self, state):
        """
        Regarde tous les zéros dans le state et pour chaque zéro, demande un
        mouvement vers chaque direction, envoie un couple (action, state) si
        le mouvement est valide.
        In this problem, each move cost 1. We don't need to specify the action since
        it's no relevant to the compute of the path cost. So successor will yield (None, state)
        """
        pass
    

    def print_conf(self):
        """
        Convertis la representation interne d'une configuration en celle donnée 
    
        """ 
        pass
    
    
    def parse_init(self):
        """
        Parse une configuration reçue en entrée en une represation valide pour
        l'utilisation du programme.
        """
        IO = IO(path)
        i = 0
        IO.init_reader()
        
        for line in IO.file:
            j = 0
            linestate = {}
            
            for char in line:
                linestate [j] = char
                j += 1
                
            self.initial[i] = linestate
            i += 1
            
    def sol_format(self, nodeList):
        """
        Crée les lignes à entrer dans le fichier solution sous forme de string
        et les yield successivement, en ajoutant une ligne vide pour chaque
        changement de noeud.
        """
        for node in nodeList:
            
            for line in node.state:
                outLine = ""
                for char in line:
                    outLine += char
                yield outLine
            yield ""
        
            
            

###################### Launch the search #########################
    
problem=PuzzleProblem(sys.argv[1])
#example of bfs search
node=breadth_first_graph_search(problem)
#example of print
path=node.path()
path.reverse()
for n in path:
    print(n.state) #assume that the __str__ function of states output the correct format

        
