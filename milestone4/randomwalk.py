'''
Created on 27 nov. 2012

@author: Florentin
'''

from search import *
from state import *

class TravelingSalesman(Problem):
    
    def __init__(self, initial, goal=None):
        self.state_init = State(initial)        
    def successor(self, state):
        yield (None, State(self.state_init.swap_all()))
    def value(self,state):
        """Compute the path value"""
        return state.compute_path()
    
if __name__ == "__main__":
    

    initial = [] # to be found with greedy method, leowlo-lo
    
    salesman = TravelingSalesman(initial)
    result = random_walk(salesman)
    print(result)
    
    