'''
Created on 27 nov. 2012

@author: Florentin
'''

from search import *
from state import *
from parserCity import *
from GreedySearch import *
from time import time


class TravelingSalesman(Problem):
    
    def __init__(self, initial,matrice, goal=None):
        self.initial= State(initial,matrice)
        self.matrice = matrice  
    def successor(self, state):
        i = 0
        previous_state = self.initial     
        while i < len(self.initial.vertices)-1:
            j=i+1
            while j < len(self.initial.vertices):
                previous_state.clone().swap(i, j)
                next_state = State(previous_state.vertices[:],self.matrice)
                yield (None, next_state)
                previous_state = next_state
                j+=1
            i+=1
    def value(self,state):
        """Compute the path value"""
        return state.compute_path(state.vertices)
    
def random_walk_override(problem, limit=100, callback=None):
    """Perform a random walk in the search space and return the best solution
    found. The returned value is a Node.
    If callback is not None, it must be a one-argument function that will be
    called at each step with the current node.
    """
    listofval = []
    current = LSNode(problem, problem.initial, 0)
    best = current
    for step in range(limit):
        #########
        listofval += [-current.value()]
        #########
        if callback is not None:
            callback(current)
        current = random.choice(list(current.expand()))
        if current.value() > best.value():
            best = current
    return [best, listofval]
    
if __name__ == "__main__":
    
    parser = Parser(sys.argv[1])
    matrice = parser.parse_line()
    N = matrice[0][0]
    initial = Greedy(N,matrice[1:], 1)
    salesman = TravelingSalesman(initial,matrice[1:])
    
    #print(-salesman.value(salesman.initial))
    start = time()
    rand_result = random_walk_override(salesman)
    result = rand_result[0]
    stop = time()
    interval = stop-start
    #print("Temps ecoule : ", format(interval)," seconde(s)")
    #print(result.state.vertices)
    #print("Cout : ",format(-result.problem.value(result.state)))
    #print("step : ",format(result.step))
#    print(format(interval))
#    print(format(-result.problem.value(result.state)))
#    print(format(result.step))
    print(rand_result[1]) 
    