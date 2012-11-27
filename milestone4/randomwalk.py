'''
Created on 27 nov. 2012

@author: Florentin
'''

from search import *

class StupidTravelingSalesman(Problem):
    
    def __init__(self, initial, goal=None):
        self.closed = dict()
        self.closed[initial] = True
    
    def successor(self, state):
        pass
    
    