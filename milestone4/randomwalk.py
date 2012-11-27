'''
Created on 27 nov. 2012

@author: Florentin
'''

from search import *

class StupidTravelingSalesman(Problem):
    
    def __init__(self, initial, goal=None):
        self.closed = dict()
        state_init = State(initial)
        
        self.closed[state_init] = True
    
    def successor(self, state):
        pass
    
    