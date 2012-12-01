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
                previous_state.swap(i, j)
                next_state = State(previous_state.vertices[:],self.matrice)
                yield (None, next_state)
                previous_state = next_state
                j+=1
            i+=1
    def value(self,state):
        """Compute the path value"""
        return state.compute_path()
    
if __name__ == "__main__":
    
    parser = Parser("tsp_instances/att48.tsp")
    matrice = parser.parse_line()
    N = matrice[0][0]
    initial = Greedy(N,matrice[1:], 1)
    salesman = TravelingSalesman(initial,matrice[1:])
    
    print(-salesman.value(salesman.initial))
    
    start = time()
    result = random_walk(salesman)
    stop = time()
    interval = stop-start
    print("Temps ecoule : ", format(interval)," seconde(s)")
    print(result.state.vertices)
    print("Cout : ",format(-result.problem.value(result.state)))
    print("step : ",format(result.step))
    
    