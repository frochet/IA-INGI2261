'''
Created on 28 nov. 2012

@author: Florentin
'''
from search import *
from state import *

class TravelingSalesman(Problem):
   
    def __init__(self, initial, goal=None):
        self.state = State(initial)
    def successor(self, state):
        yield (None, State(self.state_init.swap_best()))
    def value(self,state):
        """Compute the path value"""
        return state.compute_path()
    
if __name__ == "__main__":
    
    initial = [] # to be found with greedy method, leowlo-lo
    
    salesman = TravelingSalesman(initial)
    i = 0
    result = salesman.successor(state)
    best = result[1].value()
    best_list = result[1].vertices
    while i < 100 :
        result = salesman.successor(state)
        if result[1].value() < best :
            best = result[1]
            best_list = result[1].vertices
        i+=1
        
    print(best_list)
    print(best)