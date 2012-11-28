'''
Created on 27 nov. 2012

@author: Florentin
'''

from search import *
from state import *

class StupidTravelingSalesman(Problem):
    
    def __init__(self, initial, goal=None):
        self.closed = dict()
        self.state_init = State(initial)
        self.closed[self.state_init] = True
    def successor(self, state):
        list = self.state_init.swap()
        while list :
            newState = State(list)
            if newState not in self.closed :
                self.closed[newState] = True
                yield (None, newState)
                
            
    
    def value(self,state):
        """Compute the path value"""
        return state.comput_path()
    
    
if __name__ == "__main__":
    
    initial = [] # to be found with greedy method, léowlo-lo
    
    salesman = StupidTravelingSalesman(initial)
    result = random_walk(salesman)
    print(result)
    
    