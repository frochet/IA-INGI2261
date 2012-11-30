'''
Created on 29 nov. 2012

@author: Florentin
'''
from search import *
from state import *

class TravelingSalesman(Problem):
   
    def __init__(self, initial, goal=None):
        self.state = State(initial)
    def successor(self, state):
        yield (None, State(self.state_init.swap_random_from_bests()))
    def value(self,state):
        """Compute the path value"""
        return state.compute_path()
    